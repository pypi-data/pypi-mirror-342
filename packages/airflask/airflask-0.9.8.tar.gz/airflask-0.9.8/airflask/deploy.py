import os
import subprocess
import getpass  
import re
import multiprocessing
import psutil
import time
import socket

def optimal_host(venv_path, app_path, power):
    print("Running tests to identify hosting requirements")
    cores = multiprocessing.cpu_count()
    workers = ( 2 * cores + 1)
    def get_ram_stats():
        total_gb = psutil.virtual_memory().total / (1024 ** 3)
        available_gb = psutil.virtual_memory().available / (1024 ** 3)
        return total_gb, available_gb


    total_ram, available_before = get_ram_stats()
    print(f"Available RAM: {available_before:.2f} GB")

    process = subprocess.Popen(
        [f"{venv_path}/bin/gunicorn", "gunicorn", "wsgi:app", "--workers", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=app_path
    )

    time.sleep(3)

    # Gunicorn RAM usage
    
    available_after = psutil.virtual_memory().available / (1024 ** 3)

    print(f"Available RAM (post): {available_after:.2f} GB")
    print(f"Gunicorn RAM usage: {abs((available_after) - (available_before)):.2f} MB")
    gunicorn_ram = abs((available_after) - (available_before))
    process.terminate()
    process.wait()
    if gunicorn_ram * workers > ((available_after*1024)-250):
        print("Low ram, reducing workers")
        workers -= 1
    workers = str(workers)
    if power == "high":
        threads = "16"
        connections = "4000"
    elif power == "low":
        threads = "4"
        workers = "2"
    else:
        threads = "8"
        connections = "2000"

    return workers, threads, connections 
def get_private_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "An error occured while fetching ip address."
def get_public_ip():
    try:
        return subprocess.check_output(["curl", "-s", "https://checkip.amazonaws.com"]).decode().strip()
    except Exception:
        return get_private_ip()
        
def stopapp(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    with open(log_file, 'r') as file:
        appname = file.read()
    subprocess.run(["sudo", "systemctl", "stop", appname], stdout=subprocess.DEVNULL)
    
    
def restartapp(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    with open(log_file, 'r') as file:
        appname = file.read()
    subprocess.run(["sudo", "systemctl", "restart", appname], stdout=subprocess.DEVNULL)
    
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], stdout=subprocess.DEVNULL)

def run_deploy(app_path, domain, apptype, power, ssl, noredirect):

    app_file = os.path.join(app_path, "app.py")

    if not os.path.isfile(app_file):
        print("app.py does not exists at provided path, please rename your main flask file to app.py - Airflask")    
        return 0
    if not domain: 
        ssl = None
        domain = "_"
    nginx_default = "/etc/nginx/sites-enabled/default"
    if os.path.exists(nginx_default):
        subprocess.run(["sudo", "rm", nginx_default])
    app_name = os.path.basename(os.path.abspath(app_path))
    service_file = f"/etc/systemd/system/{app_name}.service"
    nginx_conf = f"/etc/nginx/sites-available/{app_name}"
    nginx_link = f"/etc/nginx/sites-enabled/{app_name}"
    
    print(f"📦 Deploying {app_name}...")

    print("🔧 Installing dependencies...")
    subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "apt", "install", "-y", "python3-venv", "python3-pip", "nginx"], stdout=subprocess.DEVNULL)

    venv_path = os.path.join(app_path, "venv")
    print("🐍 Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", venv_path], stdout=subprocess.DEVNULL)
    
    print("📦 Installing Flask, Gunicorn and other specified packages in requirements.txt...")
    subprocess.run([f"{venv_path}/bin/pip", "install", "flask", "gunicorn"], stdout=subprocess.DEVNULL, cwd=app_path)
    req_file = os.path.join(app_path, "requirements.txt")

    if os.path.exists(req_file):    
        subprocess.run([f"{venv_path}/bin/pip", "install", "-r", "requirements.txt"],stdout=subprocess.DEVNULL, cwd=app_path)
    else:
        print(f"Requirements.txt NOT FOUND at {app_path}, may cause dependency errors.")
    wsgi_path = os.path.join(app_path, "wsgi.py")
    if not os.path.exists(wsgi_path):
        print("📝 Creating wsgi.py...")
        with open(wsgi_path, "w") as f:
            f.write(f"from app import app\n\nif __name__ == '__main__':\n    app.run()")
    username = getpass.getuser()
    workers, threads, connections  = optimal_host(venv_path, app_path, power)
    print(f"Total workers: {workers}")
    host_type = {
        "default": f"--workers {workers}  -k gthread  --threads {threads}",
        "chatapp": f"--workers {workers}  -k gevent  --worker-connections {connections}",
        "cpubound": f"--workers {workers}  -k sync "
    }
    if not apptype:
        apptype = "default"
    if not host_type[apptype]:
        apptype = "default"
        print("Invalid app type selected, switching to default")
    exec_gunicorn = host_type[apptype]
    service_config = f"""[Unit]
    Description=Gunicorn instance to serve {app_name}
    After=network.target

    [Service]
    User={username}
    Group=www-data
    WorkingDirectory={app_path}
    ExecStart={venv_path}/bin/gunicorn {exec_gunicorn} --bind unix:{app_path}/{app_name}.sock wsgi:app

    [Install]
    WantedBy=multi-user.target
    """

    nginx_confmain = "/etc/nginx/nginx.conf"

    with open(nginx_confmain, "r") as file:
        config = file.read()

    updated_config = re.sub(r"user\s+\S+;", f"user {username};", config)

    with open(nginx_confmain, "w") as file:
        file.write(updated_config)

    print(f"Username updated in nginx.conf to {username}")
    with open('airflask.log','w') as file:
        file.write(app_name)
    with open("service_file.tmp", "w") as f:
        f.write(service_config)
    subprocess.run(["sudo", "rm", "/etc/nginx/sites-enabled/default"])
    subprocess.run(["sudo", "mv", "service_file.tmp", service_file], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "start", app_name], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "enable", app_name], stdout=subprocess.DEVNULL)

    nginx_config = f"""server {{
    listen 80;
    server_name {domain};

    location / {{
        include proxy_params;
        proxy_pass http://unix:{app_path}/{app_name}.sock;
        }}
    }}"""
    with open("nginx_conf.tmp", "w") as f:
        f.write(nginx_config)
    subprocess.run(["sudo", "mv", "nginx_conf.tmp", nginx_conf], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ln", "-s", nginx_conf, nginx_link], stdout=subprocess.DEVNULL)
    import json

    # Folder and file path
    dir_path = "/var/airflask"
    file_path = os.path.join(dir_path, "airflask.txt")

    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    # Define a list of apps (the list you want to add or update)
    new_apps = [
        [app_name, app_path],
    ]

    # Check if the file exists and read its content if it does
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            # Load the existing list of apps from the file
            apps = json.load(file)
    else:
        # If the file doesn't exist, start with an empty list
        apps = []

    # Now add the new apps to the list
    apps.extend(new_apps)

    # Write the updated list back to the file
    with open(file_path, "w") as file:
        # Save the updated list to the file in JSON format
        json.dump(apps, file)
    if ssl:
        print("Getting an ssl certificate for you")
        subprocess.run(["sudo", "apt", "install", "certbot", "python3-certbot-nginx"], stdout=subprocess.DEVNULL)
        if noredirect:
            subprocess.run(["sudo", "certbot", "--nginx", "--no-redirect"], stdout=subprocess.DEVNULL)
        else:
            subprocess.run(["sudo", "certbot", "--nginx", "--redirect"], stdout=subprocess.DEVNULL)
        subprocess.run(["sudo", "bash", "-c", 'echo "0 0,12 * * * certbot renew --quiet && systemctl reload nginx" | crontab -'], stdout=subprocess.DEVNULL)

    subprocess.run(["sudo", "systemctl", "restart", "nginx"], stdout=subprocess.DEVNULL)
    print("Please do not remove airflask.log file")
    ip_address = get_private_ip()
    if domain  == "_":
        domain = ip_address
    print(f"✅ Deployment completed! App with name '{app_name}' is live at: http://{domain}")
    if ssl:
        print(f"Also live at: https://{domain}")
