import os,sys,time
import struct


#Takes in binary format and emits String Format
#def PrintGUID(CLSID):
#    if len(CLSID)!=16:
#        return "{invalid}"
#    
#    sGuid = "{"
#    for i in range(0,16):
#        Byte = CLSID[i]
        


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
#print GUID in the proper format here
#-----------------------------------------------------
AppNameOffset = struct.unpack("H",fCon[20:22])[0]
if AppNameOffset >= inFSize or AppNameOffset + 2 >= inFSize:
    print "Error reading Application name"
else:
    len_s = fCon[AppNameOffset:AppNameOffset+2]
    len_ = ((struct.unpack("H",len_s))[0])*2
    if AppNameOffset + len_ >= inFSize:
        print "Error reading application name"
    else:
        AppName_ = fCon[AppNameOffset + 2:AppNameOffset + 2 + len_]
        AppName = AppName_.decode('utf-16')
        print "Application name: " + AppName
        OffSet = AppNameOffset + 2 + len_
        if OffSet >= inFSize or OffSet + 2 >= inFSize:
            print "Error reading Parameters"
        else:
            len_s = fCon[OffSet:OffSet+2]
#----------------------------------------------------
TriggerOffset = struct.unpack("H",fCon[22:24])[0]
if TriggerOffset >= inFSize or TriggerOffset + 2 >= inFSize:
    print "Error reading trigger info"
else:
    NumOfTriggers = struct.unpack("H",fCon[TriggerOffset:TriggerOffset+2])[0]
    TriggerOffset += 2
    if NumOfTriggers == 0:
        print "Warning: no triggers were found"
    else:
        #loop for reading triggers
        t = 0
        while TriggerOffset < inFSize:
            TriggerSize = struct.unpack("H",fCon[TriggerOffset:TriggerOffset+2])[0]
            if TriggerOffset + TriggerSize > inFSize:
                print "Error reading trigger info #" + str(t)
            else:
                TriggerInfo = fCon[TriggerOffset:TriggerOffset+TriggerSize]
            
            t = t + 1
        
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
print sSystemTime
#-------------------------------------------------
Instances = (struct.unpack("H",fCon[68:70]))[0]
print "Number of instances: " + str(hex(Instances))
#-------------------------------------------------
