import subprocess
import datetime

now = datetime.datetime.now()


def run_application(active):
    app_check = False
    if active.lower() == "on":
        try:
            subprocess.Popen((
                r"cd C:\\mslearn-tailspin-spacegame-web-master && dotnet run --configuration Release --no-build --project Tailspin.SpaceGame.Web"),
                shell=True)
            app_check = True
        except subprocess.CalledProcessError:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't start application.")
    if active.lower() == "off":
        try:
            subprocess.Popen(r"taskkill /IM Tailspin.SpaceGame.Web.exe /f", shell=True)
            app_check = True
        except subprocess.CalledProcessError:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't shutdown application.")
    return app_check
