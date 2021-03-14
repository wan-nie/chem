C     ===================
C     PGEPOL  Version 3
C     Valencia 1993.
C     ===================
C     This program prepares the coordinate file needed by GEPOL from
C     other types of coordinates files.
C     -------------------------------------------------------------
      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT INTEGER*4 (I-N)

      CHARACTER*80 FILE1
      CHARACTER*76 TIT


C  Prepare coordinates and radii for gepol 
    2 WRITE(*,*)'Change format of coordinates file in GEPOL format'
      WRITE(*,*)'Select an option'
      WRITE(*,*)'PDB                      into GEPOL ==> 1' 
      WRITE(*,*)'CHARMM                   into GEPOL ==> 2'
      WRITE(*,*)'GROMOS                   into GEPOL ==> 3'
      WRITE(*,*)'GEPOL into GEPOL new set of radii   ==> 6'
      READ(*,*,ERR=2)IOP2
      IF((IOP2.LT.1).OR.(IOP2.GT.6)) GO TO 2

      IF(IOP2.EQ.1)CALL PDB 
      IF(IOP2.EQ.2)CALL CHARMM
      IF(IOP2.EQ.3)CALL GROMOS
      IF(IOP2.EQ.4)CALL DISCOVER
      IF(IOP2.EQ.5)CALL CINT
      IF(IOP2.EQ.6)CALL CHRAD
	 

      STOP
      END

C
      SUBROUTINE PDB
C************************************************************************  
      IMPLICIT INTEGER*4 (I-N)
      
      PARAMETER (MAXLIB=500,MAXNAT=20000)

      CHARACTER*80 LINE,FILE1,FILE3
      CHARACTER*4 LATOM,LRES,ATN,REN
      CHARACTER*3 TRE
      CHARACTER*1 SEN,SEN1,U,UNK1,UNK2

      DIMENSION LATOM(MAXLIB),LRES(MAXLIB),RADI(MAXLIB)
      DIMENSION IAT(MAXNAT),ATN(MAXNAT),REN(MAXNAT),SEN(MAXNAT)
      DIMENSION IRE(MAXNAT),X(MAXNAT),Y(MAXNAT),Z(MAXNAT)
C
C read coor file
    2 WRITE(*,*)' Name of the file with coordinates'
      READ(*,'(A)')FILE1
      OPEN(UNIT=1,NAME=FILE1,FORM='FORMATTED',STATUS='OLD',ERR=2)

C Read library
      CALL LIBRARY(MAXLIB,LATOM,LRES,RADI,NLIB)

C Out put file name
    3 WRITE(*,*)' Give GEPOL coord. file'
      READ(*,'(A)')FILE3
      OPEN(UNIT=3,NAME=FILE3,FORM='FORMATTED',STATUS='NEW',ERR=3)
      
      WRITE(*,*)' Give a title'
      READ(*,'(A)')LINE
      WRITE(3,'(2A)')'*',LINE

C Read Coordinates

      I=0
    1 READ(1,'(A)',END=4)LINE
    
      IF ((LINE(1:6).EQ.'ATOM  ').OR.(LINE(1:6).EQ.'HETATM'))THEN
  
      I=I+1
      READ (LINE(7:80),'(I5,1X,5A,I4,A,3X,3F8.3)',END=4) 
     &  IAT(I),U,TRE,UNK1,REN(I),SEN(I),IRE(I),UNK2,X(I),Y(I),Z(I)

      
      IF((U.EQ.' ').OR.(U.EQ.'1').OR.(U.EQ.'2').OR.(U.EQ.'3'))THEN
       ATN(I)=TRE//U
      ELSE
       ATN(I)=U//TRE
      END IF
      
      IF((UNK1.NE.' ').OR.(UNK2.NE.' ')) THEN
      WRITE(6,'(2A)')' %%%-WARN-%%% ',LINE
      END IF

      END IF
      GO TO 1
    4 CONTINUE
    
      NATOM=I-1
      WRITE(3,'(I8)')NATOM


      SEN1='*'
      ISE1=0
      DO I=1,NATOM

       IF(SEN(I).EQ.SEN1)THEN
         ISE=ISE1
       ELSE
         SEN1=SEN(I)
         ISE1=ISE1+1
         ISE=ISE1
       END IF
       
      
         DO J=1,NLIB
           IF((REN(I).EQ.LRES(J)).AND.(ATN(I).EQ.LATOM(J)))THEN
             R=RADI(J)
             GO TO 5
           END IF
         END DO
 
	      WRITE(*,'(A,2I5,2(1X,A))')
     &       '**ATOM NOT DEFINED**',IAT(I),IRE(I),REN(I),ATN(I)
              R=999.999900E0
    5        CONTINUE
       WRITE(3,'(4F10.5,I8,1X,A,I7,1X,A,I3,1X,A)')
     & X(I),Y(I),Z(I),R,IAT(I),ATN(I),IRE(I),REN(I),ISE,SEN(I)

      END DO

      CLOSE(1)
      CLOSE(3)
      RETURN 
      END
C    
      
C
      SUBROUTINE CHARMM
C************************************************************************
      IMPLICIT INTEGER*4 (I-N)
      
      PARAMETER MAXLIB=500

      CHARACTER*80 LINE,FILE1,FILE3
      CHARACTER*4 LATOM,LRES,ATN,REN,SEN,SEN1

      DIMENSION LATOM(MAXLIB),LRES(MAXLIB),RADI(MAXLIB)

C
C read coor file
    2 WRITE(*,*)' Name of the file with coordinates'
      READ(*,'(A)')FILE1
      OPEN(UNIT=1,NAME=FILE1,FORM='FORMATTED',STATUS='OLD',ERR=2)

C Source of the radii
    4 WRITE(*,*)' The radii will be taken from:'
      WRITE(*,*)' a library                       ==> 1'
      WRITE(*,*)' the last column of charmm file == > 2'
      READ(*,*,ERR=4)IOPR

C Read library
      IF(IOPR.EQ.1)CALL LIBRARY(MAXLIB,LATOM,LRES,RADI,NLIB)
C Out put file name
    3 WRITE(*,*)' Give GEPOL coord. file'
      READ(*,'(A)')FILE3
      OPEN(UNIT=3,NAME=FILE3,FORM='FORMATTED',STATUS='NEW',ERR=3)


    1 READ(1,'(A)')LINE

      IF (LINE(1:1).EQ.'*')THEN
      WRITE(3,'(A)')LINE
      GO TO 1
      END IF
      
      READ(LINE(1:5),'(I5)') NATOM
      WRITE(3,'(I8)')NATOM

      SEN1='****'
      ISE1=0
      DO I=1,NATOM

       READ (1,'(2I5,2(1X,A),3F10.5,1X,A,5x,F10.5)') 
     &  IAT,IRE,REN,ATN,X,Y,Z,SEN,PRAD

       IF(SEN.EQ.SEN1)THEN
         ISE=ISE1
       ELSE
         SEN1=SEN
         ISE1=ISE1+1
         ISE=ISE1
       END IF
       
       IF (IOPR.EQ.1) THEN
         DO J=1,NLIB
           IF((REN.EQ.LRES(J)).AND.(ATN.EQ.LATOM(J)))THEN
             R=RADI(J)
             GO TO 5
           END IF
         END DO
         WRITE(*,'(A,2I5,2(1X,A))')
     &       '**ATOM NOT DEFINED**',IAT,IRE,REN,ATN
         R=999.999900E0
    5        CONTINUE
       ELSE
         R=PRAD
       END IF
       WRITE(3,'(4F10.5,I8,1X,A,I7,1X,A,I3,1X,A)')
     &          X,Y,Z,R,IAT,ATN,IRE,REN,ISE,SEN
      END DO

      CLOSE(1)
      CLOSE(3)
      RETURN 
      END
C
      SUBROUTINE GROMOS
C************************************************************************      
      IMPLICIT INTEGER*4 (I-N)
      
      PARAMETER MAXLIB=500

      LOGICAL NANO
      CHARACTER*80 LINE,FILE1,FILE3
      CHARACTER*4 LATOM,LRES,ATN,REN,SEN,SEN1
      CHARACTER*1 U

      DIMENSION LATOM(MAXLIB),LRES(MAXLIB),RADI(MAXLIB)

C
C read coor file
    2 WRITE(*,*)' Name of the file with coordinates'
      READ(*,'(A)')FILE1
      OPEN(UNIT=1,NAME=FILE1,FORM='FORMATTED',STATUS='OLD',ERR=2)

C Source of the radii
    4 WRITE(*,*)' Are the coor. in nanometers?(Y/N)'
      READ(*,'(A)',ERR=4)U
      IF(U.EQ.'Y')THEN
        WRITE(*,*)' The coordinates will be converted to Angstrom'
        NANO=.true.
      ELSE IF(U.EQ.'N')THEN
        NANO=.false.
      ELSE
        GO TO 4
      END IF

C Read library
      CALL LIBRARY(MAXLIB,LATOM,LRES,RADI,NLIB)
      
C Out put file name
    3 WRITE(*,*)' Give GEPOL coord. file'
      READ(*,'(A)')FILE3
      OPEN(UNIT=3,NAME=FILE3,FORM='FORMATTED',STATUS='NEW',ERR=3)
      

      READ(1,'(A)')LINE
      WRITE(3,'(2A)')'*',LINE

      READ(1,'(I5)') NATOM
      WRITE(3,'(I8)')NATOM

      SEN='A   '
      ISE=1
      
      DO I=1,NATOM

       READ (1,'(I5,A,A,x,A,I5,3F8.3)')IRE,REN,U,ATN,IAT,X,Y,Z
         IF(U.NE.' ')THEN
	 WRITE(*,'(5A)')
     &   '%%-Warn-%%',REN,U,' has been truncated to ',REN
         END IF
	 
         IF(NANO)THEN
	 X=X*10
	 Y=Y*10
	 Z=Z*10
	 END IF
	 
         DO J=1,NLIB
           IF((REN.EQ.LRES(J)).AND.(ATN.EQ.LATOM(J)))THEN
             R=RADI(J)
             GO TO 5
           END IF
         END DO
         WRITE(*,'(A,2I5,2(1X,A))')
     &       '**ATOM NOT DEFINED**',IAT,IRE,REN,ATN
         R=999.999900E0
    5        CONTINUE

       WRITE(3,'(4F10.5,I8,1X,A,I7,1X,A,I3,1X,A)')
     &          X,Y,Z,R,IAT,ATN,IRE,REN,ISE,SEN
      END DO

      CLOSE(1)
      CLOSE(3)

      RETURN 
      END

C
      SUBROUTINE DISCOVER
      
      IMPLICIT INTEGER*4 (I-N)
      WRITE(*,*)'******* Subroutine not ready yet!!!!!!!!'
      
      RETURN 
      END
      
C
      SUBROUTINE CINT
      
      IMPLICIT INTEGER*4 (I-N)
      WRITE(*,*)'******* Subroutine not ready yet!!!!!!!!'
      
      RETURN 
      END
      
C
      SUBROUTINE CHRAD
C************************************************************************     
      IMPLICIT INTEGER*4 (I-N)
      
      LOGICAL NANO
      CHARACTER*80 LINE,FILE1,FILE3
      CHARACTER*4 LATOM,LRES,ATN,REN,SEN,SEN1
      CHARACTER*1 U

      PARAMETER MAXLIB=500

      DIMENSION LATOM(MAXLIB),LRES(MAXLIB),RADI(MAXLIB)

C
C read coor file
    2 WRITE(*,*)' Name of the file with coordinates'
      READ(*,'(A)')FILE1
      OPEN(UNIT=1,NAME=FILE1,FORM='FORMATTED',STATUS='OLD',ERR=2)


C Read library
      CALL LIBRARY(MAXLIB,LATOM,LRES,RADI,NLIB)
      
C Out put file name
    3 WRITE(*,*)' Give name for new file'
      READ(*,'(A)')FILE3
      OPEN(UNIT=3,NAME=FILE3,FORM='FORMATTED',STATUS='NEW',ERR=3)
      
    1 READ(1,'(A)')LINE

      IF (LINE(1:1).EQ.'*')THEN
      WRITE(3,'(A)')LINE
      GO TO 1
      END IF
      
      READ(LINE(1:8),'(I8)') NATOM
      WRITE(3,'(I8)')NATOM

      
      DO I=1,NATOM
       READ(1,'(4F10.5,I8,1X,A,I7,1X,A,I3,1X,A)')
     &          X,Y,Z,R,IAT,ATN,IRE,REN,ISE,SEN
	 
         DO J=1,NLIB
           IF((REN.EQ.LRES(J)).AND.(ATN.EQ.LATOM(J)))THEN
             R=RADI(J)
             GO TO 5
           END IF
         END DO
         WRITE(*,'(A,2I5,2(1X,A))')
     &       '**ATOM NOT DEFINED**',IAT,IRE,REN,ATN
         R=999.999900E0
    5        CONTINUE

       WRITE(3,'(4F10.5,I8,1X,A,I7,1X,A,I3,1X,A)')
     &          X,Y,Z,R,IAT,ATN,IRE,REN,ISE,SEN
      END DO

      CLOSE(1)
      CLOSE(3)

      RETURN 
      END

C
      SUBROUTINE LIBRARY(MAXLIB,LATOM,LRES,RADI,NLIB)
C************************************************************************
      IMPLICIT INTEGER*4 (I-N)

      CHARACTER*80 LINE,FILE2
      CHARACTER*4 LATOM,LRES

      DIMENSION LATOM(MAXLIB),LRES(MAXLIB),RADI(MAXLIB)

      
    5 WRITE(*,*)' Name of the library file'
      READ(*,'(A)')FILE2
      OPEN(UNIT=2,NAME=FILE2,FORM='FORMATTED',STATUS='OLD',ERR=5)

    1 READ(2,'(A)')LINE
      IF(LINE(1:1).EQ.'*')THEN
      WRITE(*,'(A)')LINE
      GO TO 1
      END IF
 
      I=1
      READ(LINE(1:80),'(A,2X,A,F10.5)')LATOM(I),LRES(I),RADI(I)
    2 I=I+1
      READ(2,'(A,2X,A,F10.5)',END=3)LATOM(I),LRES(I),RADI(I)
      GO TO 2
    3 CONTINUE
      CLOSE(2)
      NLIB=I-1

      IF(NLIB.GT.MAXLIB) GO TO 4
      RETURN

    4 WRITE(*,*) '***ERROR*****NLIB .GT.MAXLIB'
      STOP
      END
