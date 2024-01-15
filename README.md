# Team-Vision
This Repo is dedicated to Team Vision regarding our group project for Step Presentation 2. <br/>
Create env

<b>1)</b> Start with Template.py were we create the folder structure and necessary files to support our project and pipelining
<br/> run  >python Template.py <br/>

<b>2)</b>python setup.py  Since our project is also a package ,and we have seen many library having such format <a href="https://pypi.org/project/seaborn/"/> 
<br/>to Creating such structure we use setup.py. <br/>

<b>3)</b> for the metadata we use <b>setup.cfg</b> weher wee mentioned Licence ,OS,minimum python version,options where we need some third party dependency.
</br>

<b>4)</b>tox.ini since we have written the code for os independent and python version specified we write automatated test to handle this in tox.ini<br/>
where it creats test environemnt for specified version and test all the specified task.automated test environment.

<b>5)</b> create the environment init_setup.sh</br> for the environment setup and run it using <h4> bash init_setup.sh</h4> <br/>

<b>6) </b> Writing Logger to print log of our task<br/>
<b>7) </b> Custom Exception is written <br/>
<b>8)</b>Entity for the data ingestion<br/>
<b>9)</b>Path to Logger src/ASLD_step2/logger</br>
<b>10)</b>Path to Exception src/ASLD_step2/Exception</br>
<b>11)</b>Path to read Yaml file and create directories src/ASLD_step2/utils</br>

<b> Steps to  run the project </b>
<ul>bash init_setup.sh</ul>
<ul>check conda is activated or not</ul>
<ul>manual activation, conda actiate ./env</ul>
<ul>python path/to/app.py</ul>
<ul>0.0.0.0:8002</ul>
