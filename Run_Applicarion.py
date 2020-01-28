import subprocess
import datetime

now = datetime.datetime.now()


# The run_application function open a subprocess for cmd.
# If the active value equal to "on" that application will be started.
# If the active value equal to "off" that application process will be terminated.
# AT the end, the function return the status (Pass/Fail).
def run_application(active):
    status = ""
    if active.lower() == "on":
        try:
            subprocess.Popen((
                r"cd C:\\mslearn-tailspin-spacegame-web-master && dotnet run --configuration Release --no-build --project Tailspin.SpaceGame.Web"),
                shell=True)
            status = "Pass"
        except subprocess.CalledProcessError:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't start application.")
            status = "Fail"
    if active.lower() == "off":
        try:
            subprocess.Popen(r"taskkill /IM Tailspin.SpaceGame.Web.exe /f", shell=True)
            status = "Pass"
        except subprocess.CalledProcessError:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't shutdown application.")
            status = "Fail"
    return status
