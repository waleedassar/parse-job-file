import os,sys,time
import struct

    
#Takes in binary format and emits String version
def PrintGUID(CLSID):
    if len(CLSID)!=16:
        return "{invalid}"
    sGuid = "{"
    DW = CLSID[0:4]
    DW0= (hex(ord(DW[0])))[2:]
    DW1= (hex(ord(DW[1])))[2:]
    DW2= (hex(ord(DW[2])))[2:]
    DW3= (hex(ord(DW[3])))[2:]
    if len(DW3) == 1:
        sGuid += "0"
    sGuid += DW3
    if len(DW2) == 1:
        sGuid += "0"
    sGuid += DW2
    if len(DW1) == 1:
        sGuid += "0"
    sGuid += DW1
    if len(DW0) == 1:
        sGuid += "0"
    sGuid += DW0
    sGuid += "-"
    W0 = CLSID[4:6]
    W0_0 = (hex(ord(W0[0])))[2:]
    W0_1 = (hex(ord(W0[1])))[2:]
    if len(W0_1) == 1:
        sGuid += "0"
    sGuid += W0_1
    if len(W0_0) == 1:
        sGuid += "0"
    sGuid += W0_0
    sGuid += "-"
    W1 = CLSID[6:8]
    W1_0 = (hex(ord(W1[0])))[2:]
    W1_1 = (hex(ord(W1[1])))[2:]
    if len(W1_1) == 1:
        sGuid += "0"
    sGuid += W1_1
    if len(W1_0) == 1:
        sGuid += "0"
    sGuid += W1_0
    sGuid += "-"
    W2 = CLSID[8:10]
    W2_0 = (hex(ord(W2[0])))[2:]
    W2_1 = (hex(ord(W2[1])))[2:]
    if len(W2_0) == 1:
        sGuid += "0"
    sGuid += W2_0
    if len(W2_1) == 1:
        sGuid += "0"
    sGuid += W2_1
    sGuid += "-"
    Last = CLSID[10:16]
    Last0 = (hex(ord(Last[0])))[2:]
    if len(Last0) == 1:
        sGuid += "0"
    sGuid += Last0
    Last1 = (hex(ord(Last[1])))[2:]
    if len(Last1) == 1:
        sGuid += "0"
    sGuid += Last1
    Last2 = (hex(ord(Last[2])))[2:]
    if len(Last2) == 1:
        sGuid += "0"
    sGuid += Last2
    Last3 = (hex(ord(Last[3])))[2:]
    if len(Last3) == 1:
        sGuid += "0"
    sGuid += Last3
    Last4 = (hex(ord(Last[4])))[2:]
    if len(Last4) == 1:
        sGuid += "0"
    sGuid += Last4
    Last5 = (hex(ord(Last[5])))[2:]
    if len(Last5) == 1:
        sGuid += "0"
    sGuid += Last5
    sGuid += "}"
    return sGuid
     
def GetOS(shOS):
    if shOS == 0x0400:
        return "Windows NT 4.0"
    elif shOS == 0x0500:
        return "Windows 2000"
    elif shOS == 0x0501:
        return "Windows XP"
    elif shOS == 0x0600:
        return "Windows Vista"
    elif shOS == 0x0601:
        return "Windows 7"
    elif shOS == 0x0602:
        return "Windows 8"
    elif shOS == 0x0603:
        return "Windows 8.1"
    return "Unknown OS version"

def GetWeekDay(iWeekDay):
    if iWeekDay == 1:
        return "Mon"
    elif iWeekDay == 2:
        return "Tue"
    elif iWeekDay == 3:
        return "Wed"
    elif iWeekDay == 4:
        return "Thu"
    elif iWeekDay == 5:
        return "Fri"
    elif iWeekDay == 6:
        return "Sat"
    elif iWeekDay == 7:
        return "Sun"
    return "N/A"

def GetWeekDaysFromFlagBits(Flags):
    Days = []
    Flags = Flags & 0xFFFF
    if Flags == 0:
        return ""
    if Flags & 0x200:
        Days.append("Sat")
    if Flags & 0x400:
        Days.append("Fri")
    if Flags & 0x800:
        Days.append("Thu")
    if Flags & 0x1000:
        Days.append("Wedn")
    if Flags & 0x2000:
        Days.append("Tue")
    if Flags & 0x4000:
        Days.append("Mon")
    if Flags & 0x8000:
        Days.append("Sun")
    NumDays = len(Days)
    if NumDays == 0:
        return ""
    else:
        r_Days = "("
        for i in range(0,NumDays):
            r_Days += Days[i]
            if i != NumDays-1:
                r_Days += "-"
        r_Days += ")"
        return r_Days
    return ""

def GetDayFromFlagBits(Flags):
    Days = []
    test = 1
    for i in range(1,32):
        NewTest = test << i
        if Flags & NewTest != 0:
            Days.append(i)
    NumDays = len(Days)
    if NumDays == 0:
        return ""
    else:
        Dayss = "("
        for ii in range(0,NumDays):
            Dayss += Days[ii]
            if ii != NumDays-1:
                Dayss += ", "
        Dayss += ")"
        return Dayss
    return ""

def GetMonthFromFlagBits(Flags):
    Months = []
    if Flags & 0x10:
        Months.append("Dec")
    if Flags & 0x20:
        Months.append("Nov")
    if Flags & 0x40:
        Months.append("Oct")
    if Flags & 0x80:
        Months.append("Sep")
    if Flags & 0x100:
        Months.append("Aug")
    if Flags & 0x200:
        Months.append("Jul")
    if Flags & 0x400:
        Months.append("Jun")
    if Flags & 0x800:
        Months.append("May")
    if Flags & 0x1000:
        Months.append("Apr")
    if Flags & 0x2000:
        Months.append("Mar")
    if Flags & 0x4000:
        Months.append("Feb")
    if Flags & 0x8000:
        Months.append("Jan")
    NumMonths = len(Months)
    if NumMonths == 0:
        return ""
    else:
        Monthss = "("
        for ii in range(0,NumMonths):
            Monthss += Months[ii]
            if ii != NumMonths-1:
                Monthss += ", "
        Monthss += ")"
        return Monthss
    return ""

def GetLiteralWeekNumber(Number):
    if Number == 1:
        return "First"
    elif Number == 2:
        return "Second"
    elif Number == 3:
        return "Third"
    elif Number == 4:
        return "Fourth"
    elif Number == 5:
        return "Last"
    return str(Number)+"th"
        
def PrintSystemTime(Time):
    if len(Time)!=16:
        print "Unknown time format"
    Year = Time[0:2]
    sYear = str(struct.unpack("H",Year)[0])
    Month = Time[2:4]
    sMonth = str(struct.unpack("H",Month)[0])
    WeekDay = Time[4:6]
    sWeekDay = GetWeekDay(struct.unpack("H",WeekDay)[0])
    Day = Time[6:8]
    sDay = str(struct.unpack("H",Day)[0])
    Hour = Time[8:10]
    sHour = str(struct.unpack("H",Hour)[0])
    Minute = Time[10:12]
    sMinute = str(struct.unpack("H",Minute)[0])
    Second = Time[12:14]
    sSecond = str(struct.unpack("H",Second)[0])
    MilliSecond = Time[14:16]
    sMilliSecond = str(struct.unpack("H",MilliSecond)[0])
    TimeDate = sWeekDay + " " + sDay + "/" + sMonth + "/" + sYear + "  " + sHour + ":" + sMinute + ":" + sSecond + ":" + sMilliSecond
    return TimeDate

if len(sys.argv)!=2:
    print "Usage: ReadJob.py input.job\r\n"
    sys.exit(-1)

inF = sys.argv[1]

if os.path.exists(inF) == False or \
   os.path.getsize(inF)==0:
    print "File does not exist or is empty\r\n"
    sys.exit(-2)

inFSize = os.path.getsize(inF)
if inFSize <= 0x44:
    print "File is too small\r\n"
    sys.exit(-3)

fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()

ProductVersion = struct.unpack("H",fCon[0:2])[0]
print "Product Version: " + str(hex(ProductVersion)) + " (" + GetOS(ProductVersion) + ")"
#-----------------------------------------------------
FormatVersion = struct.unpack("H",fCon[2:4])[0]
print "Format Version: " + str(hex(FormatVersion))
#-----------------------------------------------------
Guid = fCon[4:20]
print "Job UUID: " + PrintGUID(Guid)
#-----------------------------------------------------
AppNameOffset = struct.unpack("H",fCon[20:22])[0]
ListNames = ["Application Name","Parameters","Working Directory","Author","Comment","User Data","Reserved Data"]
Offset = AppNameOffset
iCounter = 0

while iCounter < 7:
    if Offset >= inFSize and Offset + 2 >= inFSize:
        print "Boundary error while reading " + ListNames[iCounter]
        break
    else:
        len_s = fCon[Offset:Offset+2]
        len_ = ((struct.unpack("H",len_s))[0])*2
        Offset += 2
        if len_ == 0:
            print ListNames[iCounter] + ": N/A"
        else:
            if Offset + len_ >= inFSize:
                print "Boundary error while reading " + ListNames[iCounter]
            else:
                uStrXXX = fCon[Offset:Offset + len_]
                if iCounter == 6:
                    ReservedNull = True
                    len_ = len_/2
                    Reserved = uStrXXX
                    for xxx in range(0,len_):
                        if Reserved[xxx] != "\x00":
                            print "Warning: Reserved data is not set to null"
                            ReservedNull = False
                            break
                    if ReservedNull == True:
                        print ListNames[iCounter] + ": N/A"
                else:
                    StrXXX = uStrXXX.decode('utf-16')
                    StrXXX = StrXXX.rstrip("\x00").lstrip("\x00")
                    print ListNames[iCounter] + ": " + StrXXX
                Offset += len_
    iCounter += 1
#-----------------------------------------------
print "----------------Triggers----------------"
TriggerOffset = struct.unpack("H",fCon[22:24])[0]
if TriggerOffset >= inFSize or TriggerOffset + 2 >= inFSize:
    print "Boundary error while reading trigger info"
else:
    NumOfTriggers_s = fCon[TriggerOffset:TriggerOffset+2]
    NumOfTriggers = struct.unpack("H",NumOfTriggers_s)[0]
    TriggerOffset += 2
    if NumOfTriggers == 0:
        print "Warning: no triggers were found"
    else:
        print "Number Of Triggers: " + str(NumOfTriggers)
        #loop for reading triggers
        t = 0
        while TriggerOffset < inFSize:
            print "===> Trigger #" + str(t+1)
            TriggerSize = struct.unpack("H",fCon[TriggerOffset:TriggerOffset+2])[0]
            print "TriggerSize: " + str(TriggerSize)
            if TriggerOffset + TriggerSize > inFSize:
                print "Error reading trigger info #" + str(t)
                break
            else:
                TriggerInfo = fCon[TriggerOffset:TriggerOffset+TriggerSize]
                Resv0 = struct.unpack("H",TriggerInfo[2:4])[0]
                print "Reserved1: " + str(hex(Resv0))
                #if Resv0 != 0:
                #    print "Warning: First reserved field of TRIGGER is not set to null"
                BeginYear = struct.unpack("H",TriggerInfo[4:6])[0]
                BeginMonth = struct.unpack("H",TriggerInfo[6:8])[0]
                BeginDay = struct.unpack("H",TriggerInfo[8:10])[0]
                #Don't run before
                print "First Trigger Date: " + str(BeginYear) + ":" + str(BeginMonth) + ":" + str(BeginDay)
                EndYear = struct.unpack("H",TriggerInfo[10:12])[0]
                EndMonth = struct.unpack("H",TriggerInfo[12:14])[0]
                EndDay = struct.unpack("H",TriggerInfo[14:16])[0]
                #Don't run after
                print "Last Trigger Date: " + str(EndYear) + ":" + str(EndMonth) + ":" + str(EndDay)
                StartHour = struct.unpack("H",TriggerInfo[16:18])[0]
                StartMinute = struct.unpack("H",TriggerInfo[18:20])[0]
                print "Scheduled Trigger Time: " + str(StartHour) + ":" + str(StartMinute)
                MinutesDuration = struct.unpack("L",TriggerInfo[20:24])[0]
                print "MinutesDuration: " + str(MinutesDuration)
                MinutesInterval = struct.unpack("L",TriggerInfo[24:28])[0]
                print "MinutesInterval: " + str(MinutesInterval)
                NumberOfScheduledTimes = 1
                if MinutesInterval != 0:
                    NumberOfScheduledTimes+= MinutesDuration/MinutesInterval
                print "Runs " + str(NumberOfScheduledTimes) + " times."
                Flags = struct.unpack("L",TriggerInfo[28:32])[0]
                print "Flags: " + str(hex(Flags))
                if Flags & 0x80000000:
                    print "==> TASK_TRIGGER_FLAG_HAS_END_DATE"
                if Flags & 0x40000000:
                    print "==> TASK_TRIGGER_FLAG_KILL_AT_DURATION_END"
                if Flags & 0x20000000:
                    print "==> TASK_TRIGGER_FLAG_DISABLED"
                TriggerType = struct.unpack("L",TriggerInfo[32:36])[0]
                print "TriggerType: " + str(TriggerType)
                if TriggerType == 0:
                    print "==> ONCE"
                elif TriggerType == 1:
                    print "==> DAILY"
                elif TriggerType == 2:
                    print "==> WEEKLY"
                elif TriggerType == 3:
                    print "==> MONTHLYDATE"
                elif TriggerType == 4:
                    print "==> MONTHLYDOW"
                elif TriggerType == 5:
                    print "==> EVENT_ON_IDLE"
                elif TriggerType == 6:
                    print "==> EVENT_AT_SYSTEMSTART"
                elif TriggerType == 7:
                    print "==> EVENT_AT_LOGON"
                TriggerSpec0 = struct.unpack("H",TriggerInfo[36:38])[0]
                if TriggerType == 1:
                    print "Run every: " + str(TriggerSpec0) + " day(s)"
                elif TriggerType == 2:
                    print "Run every: " + str(TriggerSpec0) + " week(s)"
                elif TriggerType == 3:
                    pass
                elif TriggerType == 4:
                    print "In " + GetLiteralWeekNumber(TriggerSpec0) + " week"
                else:
                    print "TriggerSpecific0: " + str(hex(TriggerSpec0))
                
                TriggerSpec1 = struct.unpack("H",TriggerInfo[38:40])[0]
                if TriggerType == 2:
                    print "On " + GetWeekDaysFromFlagBits(TriggerSpec1)
                elif TriggerType == 3:
                    Day_s = TriggerInfo[36:40]
                    Day_i = struct.unpack("L",Day_s)[0]
                    print "On " + GetDayFromFlagBits(Day_i)
                elif TriggerType == 4:
                    print "On " + GetWeekDaysFromFlagBits(TriggerSpec1)
                else:
                    print "TriggerSpecific1: " + str(hex(TriggerSpec1))

                TriggerSpec2 = struct.unpack("H",TriggerInfo[40:42])[0]
                if TriggerType == 3:
                    print "In " + GetMonthFromFlagBits(TriggerSpec2)
                elif TriggerType == 4:
                    print "In " + GetMonthFromFlagBits(TriggerSpec2)
                else:
                    print "TriggerSpecific2: " + str(hex(TriggerSpec2))
                    
                Padding = struct.unpack("H",TriggerInfo[42:44])[0]
                print "Padding: " + str(hex(Padding))
                Resv1 = struct.unpack("H",TriggerInfo[44:46])[0]
                print "Reserved2: " + str(hex(Resv1))
                Resv2 = struct.unpack("H",TriggerInfo[46:48])[0]
                print "Reserved3: " + str(hex(Resv2))
                TriggerOffset += TriggerSize
            t = t + 1
#----------------------------------------------------
#Print job singature if exists
print "------------ Job Signature ------------"
JobSignOffset = TriggerOffset
if JobSignOffset < inFSize:
    if JobSignOffset + 68 <= inFSize:
        JobSign = fCon[JobSignOffset:JobSignOffset+68]
        SignatureVersion = struct.unpack("H",JobSign[0:2])[0]
        t_str = "SignatureVersion: " + str(hex(SignatureVersion))
        if SignatureVersion != 1:
            t_str += "  (Warning: Must be 1)"
        print t_str
        MinClientVersion = struct.unpack("H",JobSign[2:4])[0]
        t_str = "MinClientVersion: " + str(hex(MinClientVersion))
        if MinClientVersion != 1:
            t_str += "  (Warning: Must be 1)"
        print t_str
        Hash = JobSign[4:]
        #Add code for printing hashes here
    else:
        print "Boundary error while reading Job Signature"
else:
    print "Job Signature: N/A"
print "---------------------------------------"
#----------------------------------------------------
ErrorRetryCount = struct.unpack("H",fCon[24:26])[0]
print "Error Retry Count: " + str(hex(ErrorRetryCount))
#----------------------------------------------------
ErrorRetryInterval = struct.unpack("H",fCon[26:28])[0]
print "Error Retry Interval: " + str(hex(ErrorRetryInterval))
#----------------------------------------------------
IdleDeadline = struct.unpack("H",fCon[28:30])[0]
print "Idle Deadline: " + str(hex(IdleDeadline))
#----------------------------------------------------
IdleWait = struct.unpack("H",fCon[30:32])[0]
print "Idle Wait: " + str(hex(IdleWait))
#----------------------------------------------------
Priority = struct.unpack("L",fCon[32:36])[0]
sPriority = "Priority: " + str(hex(Priority))

if Priority & 0x00800000:
    sPriority +=  " (REALTIME_PRIORITY_CLASS) "
if Priority & 0x01000000:
    sPriority += " (HIGH_PRIORITY_CLASS) "
if Priority & 0x02000000:
    sPriority += " (IDLE_PRIORITY_CLASS) "
if Priority & 0x04000000:
    sPriority += " (NORMAL_PRIORITY_CLASS) "
if Priority & 0x00800000 == 0 and \
   Priority & 0x01000000 == 0 and \
   Priority & 0x02000000 == 0 and \
   Priority & 0x04000000 == 0:
    sPriority += " (Unknown Flags) "
print sPriority
#----------------------------------------------------
MaximumRunTime = struct.unpack("L",fCon[36:40])[0]
print "Maximum Runtime: " + str(hex(MaximumRunTime))
#----------------------------------------------------
ExitCode = struct.unpack("L",fCon[40:44])[0]
print "Exit Code: " + str(hex(ExitCode))
#----------------------------------------------------
StatusCode = struct.unpack("L",fCon[44:48])[0]
sStatusCode = "Status Code: " + str(hex(StatusCode))
if StatusCode == 0x00041300:
    sStatusCode += " (SCHED_S_TASK_READY)"
elif StatusCode == 0x00041301:
    sStatusCode += " (SCHED_S_TASK_RUNNING)"
elif StatusCode == 0x00041305:
    sStatusCode += " (SCHED_S_TASK_NOT_SCHEDULED)"
else:
    sStausCode +=  " (Unknown)"
print sStatusCode
#----------------------------------------------------
Flags = struct.unpack("L",fCon[48:52])[0]
sFlags = "Flags: " + str(hex(Flags))
if Flags & 0x1:
    sFlags += " TASK_FLAG_INTERACTIVE(I)"
if Flags & 0x2:
    sFlags += " TASK_FLAG_DELETE_WHEN_DONE(DD)"
if Flags & 0x4:
    sFlags += " TASK_FLAG_DISABLED(D)"
if Flags & 0x8:
    sFlags += " TASK_FLAG_START_ONLY_IF_IDLE(SI)"
if Flags & 0x10:
    sFlags += " TASK_FLAG_KILL_ON_IDLE_END(KI)"
if Flags & 0x20:
    sFlags += " TASK_FLAG_DONT_START_IF_ON_BATTERIES(SB)"
if Flags & 0x40:
    sFlags += " TASK_FLAG_KILL_IF_GOING_ON_BATTERIES(KB)"
if Flags & 0x80:
    sFlags += " TASK_FLAG_RUN_ONLY_IF_DOCKED(RD)"
if Flags & 0x100:
    sFlags += " TASK_FLAG_HIDDEN(H)"
if Flags & 0x200:
    sFlags += " TASK_FLAG_RUN_IF_CONNECTED_TO_INTERNET(RC)"
if Flags & 0x400:
    sFlags += " TASK_FLAG_RESTART_ON_IDLE_RESUME(RI)"
if Flags & 0x800:
    sFlags += " TASK_FLAG_SYSTEM_REQUIRED(SR)"
if Flags & 0x1000:
    sFlags += " TASK_FLAG_RUN_ONLY_IF_LOGGED_ON(RL)"
if Flags & 0x2000:
    sFlags += " TASK_APPLICATION_NAME(AN)"
if Flags & 0x4000 or \
   Flags & 0x8000:
    sFlags += " Unknown flags "
print sFlags
#-------------------------------------------------
SystemTime = fCon[52:68]
sSystemTime = PrintSystemTime(SystemTime)
print "Last Run Time: " + sSystemTime
#-------------------------------------------------
Instances = (struct.unpack("H",fCon[68:70]))[0]
print "Number of instances: " + str(hex(Instances))
#-------------------------------------------------
