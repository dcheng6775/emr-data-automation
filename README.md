**Clinical Data Parser**

A local tool for automatically extracting clinical variables from cardiology and electrophysiology EMR reports. 

Privacy note: This tool runs entirely on your local machine. No patient data is ever uploaded to external servers.


**What it does**

You can upload up to 3 clinical notes, EMRs, etc. via pdf, image, or plain text, and the tool automatically extracts the following:
- name
- age
- sex
- ht
- wt
- BMI
- age 65-74?
- age 75+?
- female?
- AFib type
- Ablation type
- LVEF

Other variables to be added & current variables are in the process of being tested. 

**Requirements & How to use**

<ins>Step 1 — Download Docker Desktop</ins>

Go to https://www.docker.com/products/docker-desktop and download for your OS (Mac or Windows). 
Install and open the app, wait for a whale icon to appear in the menu bar/taskbar.

<ins>Step 2 — Download the code</ins>

Go to this GitHub repo (at https://github.com/dcheng6775/emr-data-automation) → click the green Code button in the top right corner → click Download ZIP → unzip in the Desktop.

<ins>Step 3 — Open terminal</ins>

Mac: search "Terminal" in Spotlight

Windows: search "PowerShell" in the start menu

Then type:

cd Desktop/[folder name that it was unzipped as]

(adjust the folder name to whatever it unzipped as)

as an example, if the folder name was emr-data-automation-main, you type:

cd Desktop/emr-data-automation-main


<ins>Step 4 — Run it</ins>

docker compose up --build

First time takes ~5 minutes. When it settles, open a browser and go to http://localhost:3000. You can now access the app.

<ins>Step 5 — Stopping it</ins>

Press Ctrl+C in the terminal, then run:

docker compose down
