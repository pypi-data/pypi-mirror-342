//Z21235T  JOB (ACCT,'DEPT'),'BATCH JOB',
//         CLASS=A,MSGCLASS=X,MSGLEVEL=(1,1),
//         NOTIFY=&SYSUID,REGION=0M,TIME=1440
//*********************************************************************
//* SAMPLE Z/OS BATCH JOB FOR PROCESSING TRANSACTION DATA
//* JOBNAME: Z21235T
//* CREATED: 2023-05-15
//* UPDATED: 2023-10-01
//* PURPOSE: DAILY TRANSACTION PROCESSING
//*********************************************************************
//*
//JOBLIB   DD DSN=SYS1.LINKLIB,DISP=SHR
//         DD DSN=SYS2.APPLOAD,DISP=SHR
//*
//*********************************************************************
//* STEP01 - CHECK IF CONTROL FILE EXISTS
//*********************************************************************
//STEP01   EXEC PGM=IDCAMS
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  LISTCAT ENT('PROD.CONTROL.FILE') ALL
/*
//*
//*********************************************************************
//* STEP02 - BACKUP CURRENT TRANSACTION FILE
//*********************************************************************
//STEP02   EXEC PGM=ADRDSSU,COND=(4,LT,STEP01)
//SYSPRINT DD SYSOUT=*
//TAPE     DD DSN=BACKUP.TRANS.&YYMMDD,
//            DISP=(NEW,CATLG,DELETE),
//            UNIT=TAPE,
//            DCB=(RECFM=FB,LRECL=80,BLKSIZE=32720)
//SYSIN    DD *
  DUMP DATASET(INCLUDE(PROD.TRANSACTION.DATA)) -
       OUTDDNAME(TAPE) -
       TOL(ENQF) -
       OPTIMIZE(4) -
       COMPRESS
/*
//*
//*********************************************************************
//* STEP03 - PROCESS TRANSACTION DATA
//*********************************************************************
//STEP03   EXEC PGM=TPROCESS,
//            PARM='&YYMMDD,&SYSUID,FULL',
//            COND=((4,LT,STEP01),(0,LT,STEP02))
//STEPLIB  DD DSN=APP.LOADLIB,DISP=SHR
//SYSPRINT DD SYSOUT=*
//SYSDBOUT DD SYSOUT=*
//SYSUDUMP DD SYSOUT=*
//CONTROL  DD DSN=PROD.CONTROL.FILE,DISP=SHR
//TRANSACT DD DSN=PROD.TRANSACTION.DATA,DISP=SHR
//MASTER   DD DSN=PROD.MASTER.FILE,DISP=OLD
//REPORT   DD DSN=PROD.DAILY.REPORT.&YYMMDD,
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(CYL,(50,20),RLSE),
//            DCB=(RECFM=FBA,LRECL=133,BLKSIZE=0)
//SYSIN    DD *
* PROCESS PARAMETERS
MODE=PRODUCTION
DEBUG=NO
AUDITTRAIL=YES
TIMEOUT=3600
/*
//*
//*********************************************************************
//* STEP04 - SORT AND SUMMARIZE RESULTS
//*********************************************************************
//STEP04   EXEC PGM=SORT,COND=((4,LT,STEP01),(0,LT,STEP03))
//SYSOUT   DD SYSOUT=*
//SORTIN   DD DSN=PROD.DAILY.REPORT.&YYMMDD,DISP=SHR
//SORTOUT  DD DSN=PROD.DAILY.SUMMARY.&YYMMDD,
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(CYL,(10,5),RLSE),
//            DCB=(RECFM=FB,LRECL=100,BLKSIZE=0)
//SYSIN    DD *
  SORT FIELDS=(1,10,CH,A,11,5,PD,D)
  SUM FIELDS=(16,8,PD,25,6,PD,31,8,PD)
  OPTION DYNALLOC,ZDPRINT
/*
//*
//*********************************************************************
//* STEP05 - IMS DATABASE UPDATE
//*********************************************************************
//STEP05   EXEC PGM=DFSRRC00,
//            PARM='DLI,IMSUPDT,IMSPSB01,,,,,,,,,,,N',
//            COND=((4,LT,STEP01),(0,LT,STEP04))
//STEPLIB  DD DSN=IMS.RESLIB,DISP=SHR
//         DD DSN=IMS.PGMLIB,DISP=SHR
//DFSRESLB DD DSN=IMS.RESLIB,DISP=SHR
//IMS      DD DSN=IMS.PSBLIB,DISP=SHR
//         DD DSN=IMS.DBDLIB,DISP=SHR
//IEFRDER  DD DUMMY
//DFSVSAMP DD *
BUFPOOLS 1024 8192,10 12288,10 16384,10 20480,10 24576,10
VSAMOPT  IOB=40,DMB=10,PSB=10
/*
//IMSACBA  DD DSN=IMS.ACBLIB,DISP=SHR
//SUMMARY  DD DSN=PROD.DAILY.SUMMARY.&YYMMDD,DISP=SHR
//OUTPUT   DD DSN=PROD.IMS.REPORT.&YYMMDD,
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(CYL,(5,2),RLSE),
//            DCB=(RECFM=FB,LRECL=100,BLKSIZE=0)
//SYSUDUMP DD SYSOUT=*
//SYSIN    DD *
UPDATE MODE=EXCLUSIVE
/*
//*
//*********************************************************************
//* STEP06 - CLEAN UP AND NOTIFY
//*********************************************************************
//STEP06   EXEC PGM=IKJEFT01,COND=EVEN
//SYSTSPRT DD SYSOUT=*
//SYSPROC  DD DSN=SYS1.CLIST,DISP=SHR
//SYSEXEC  DD DSN=SYS2.REXX.EXEC,DISP=SHR
//SYSTSIN  DD *
%NOTIFY JOBNAME=Z21235T USERID=&SYSUID
/*
// 