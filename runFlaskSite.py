from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/raw')
def raw():
    tempString = ""

    with open('../NODEMCU/temp.txt') as f:
        tempString = f.read()

    return tempString

@app.route('/')
def hello():

    tempString = ""
    with open('../NODEMCU/temp.txt') as f:
        tempString = f.read()

    with open('iplist.txt', 'a') as f:
        ip = request.remote_addr

        if ip.split('.')[0] != "10":
            print("IP: "+ip)
            f.write(ip+"\n")
        else:
            print("LOCAL IP -> NOT ADDED")

    site = """
    <!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>Test</h2>
<button onclick="changeUpdateRate(10)">10S Update</button>

<table>
  <tr>
    <td>Thing</td>
    <td>Temperature</td>
    <td>Last updated: </td>
  </tr>
  <tr>
    <td>Sensor1</td>
    <td id="demo"></td>
    <td id="update">dunno</td>
  </tr>
</table>


<script>

    var updateRate = 5000;

    // Load the sensor values when the page is loaded
    document.addEventListener("DOMContentLoaded", function(){
        loadDoc();
    });

    // Update the values every <updateRate> ms
    setInterval(loadDoc, updateRate);

    function loadDoc() {
        var xhttp = new XMLHttpRequest();
        
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("demo").innerHTML =
                this.responseText;
            }
        };
        
        xhttp.open("GET", "raw", true);
        xhttp.send();
        
        var dt = new Date();
        document.getElementById("update").innerHTML = dt.getHours()+"."+dt.getMinutes()+"."+dt.getSeconds()+":"+dt.getMilliseconds();
    }
    
    // Change the update rate (seconds)
    function changeUpdateRate(rate) {
        updateRate = rate*1000;
    }
</script>

</body>

</html>

    """

    return site
