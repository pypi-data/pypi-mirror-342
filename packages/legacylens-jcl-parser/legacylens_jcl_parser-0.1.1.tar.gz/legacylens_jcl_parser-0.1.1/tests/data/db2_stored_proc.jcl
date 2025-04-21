//DB2PROC  JOB (DB2,1),'DB2 PROCEDURE',CLASS=A,MSGCLASS=X,
//         MSGLEVEL=(1,1),NOTIFY=&SYSUID
//*********************************************************************
//* JCL TO CREATE AND BIND A DB2 STORED PROCEDURE
//* SYSTEM: DB2 V12
//* DATE: 2023-09-10
//*********************************************************************
//*
//JOBLIB   DD  DSN=DSN.V12.SDSNLOAD,DISP=SHR
//         DD  DSN=DSN.V12.RUNLIB.LOAD,DISP=SHR
//*
//*********************************************************************
//* STEP 1 - PRECOMPILE AND PREPARE COBOL PROGRAM
//*********************************************************************
//COMP     EXEC PGM=IKJEFT01,DYNAMNBR=20
//SYSTSPRT DD  SYSOUT=*
//SYSTSIN  DD  *
  DSN SYSTEM(DSN1)
  PREP 'DB2USER.SOURCE.COBOL(CUSTPROC)' -
       MEMBER(CUSTPROC) -
       LIB('DB2USER.OBJLIB') -
       COMPILE(COB2LIB,'DYNAM,RENT,NOOPT') -
       PRECOMP('HOST(COBOL)') -
       BIND(ACQUIRE(USE)) -
       CLIST(NONE) -
       CONNECT(DB2DEV) -
       ISOLATION(CS) -
       SQLERROR(NOPACKAGE)
  END
/*
//COB2LIB  DD  DSN=IGY.V6R3M0.SIGYCOMP,DISP=SHR
//*
//*********************************************************************
//* STEP 2 - BIND THE PACKAGE
//*********************************************************************
//BIND     EXEC PGM=IKJEFT01
//SYSTSPRT DD  SYSOUT=*
//SYSTSIN  DD  *
  DSN SYSTEM(DSN1)
  BIND PACKAGE(CUSTPKG) -
       MEMBER(CUSTPROC) -
       LIB('DB2USER.OBJLIB') -
       ISOLATION(CS) -
       VALIDATE(BIND) -
       RELEASE(COMMIT) -
       EXPLAIN(YES) -
       OWNER(DB2USER) -
       QUALIFIER(DB2USER) -
       ACTION(REPLACE) -
       CURRENTDATA(YES)
  END
/*
//*
//*********************************************************************
//* STEP 3 - CREATE THE STORED PROCEDURE
//*********************************************************************
//CRPROC   EXEC PGM=IKJEFT01
//SYSTSPRT DD  SYSOUT=*
//SYSTSIN  DD  *
  DSN SYSTEM(DSN1)
  RUN PROGRAM(DSNTIAD) PLAN(DSNTIA12) -
      LIB('DSN.V12.RUNLIB.LOAD')
  END
/*
//SYSIN    DD  *
  DROP PROCEDURE DB2USER.GET_CUSTOMER_INFO;
  
  COMMIT;
  
  CREATE PROCEDURE DB2USER.GET_CUSTOMER_INFO
    (IN  P_CUSTID      INTEGER,
     OUT P_FIRSTNAME   VARCHAR(30),
     OUT P_LASTNAME    VARCHAR(30),
     OUT P_ADDRESS     VARCHAR(100),
     OUT P_CITY        VARCHAR(30),
     OUT P_STATE       CHAR(2),
     OUT P_ZIPCODE     CHAR(10),
     OUT P_PHONE       CHAR(15))
    
    LANGUAGE COBOL
    EXTERNAL NAME CUSTPROC
    COLLID CUSTPKG
    WLM ENVIRONMENT WLMENV1
    ASUTIME NO LIMIT
    STAY RESIDENT YES
    PROGRAM TYPE MAIN
    SECURITY DB2
    COMMIT ON RETURN YES
    PARAMETER STYLE GENERAL WITH NULLS
    DYNAMIC RESULT SETS 0;
  
  COMMIT;
  
  GRANT EXECUTE ON PROCEDURE DB2USER.GET_CUSTOMER_INFO TO PUBLIC;
  
  COMMIT;
/*
//*
//*********************************************************************
//* STEP 4 - RUN VALIDATION TEST
//*********************************************************************
//TEST     EXEC PGM=IKJEFT01
//SYSTSPRT DD  SYSOUT=*
//SYSPRINT DD  SYSOUT=*
//SYSOUT   DD  SYSOUT=*
//SYSTSIN  DD  *
  DSN SYSTEM(DSN1)
  RUN PROGRAM(DSNTEP2) PLAN(DSNTEP12) -
      LIB('DSN.V12.RUNLIB.LOAD')
  END
/*
//SYSIN    DD  *
  -- Test calling the stored procedure
  CALL DB2USER.GET_CUSTOMER_INFO(
    101, -- Customer ID
    :FNAME, :LNAME, :ADDR, :CITY, :STATE, :ZIP, :PHONE);
/*
//* 