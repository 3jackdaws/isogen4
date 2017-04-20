/**
 * Created by ian on 4/14/17.
 */

var Terminal = {
    in:document.getElementById("input"),
    out:document.getElementById("console"),
    running:null,
    exec:function () {
        var commandLine = Terminal.in.value;
        Terminal.in.value = "";
        Terminal.write(">"+commandLine+"\n");
        if(Terminal.running) Terminal.running(commandLine);
        else{
            var arguments = commandLine.split(" ");
            var command = arguments[0];
            if(command in Terminal.commands){
                Terminal.commands[command](arguments);
            }else{
                Terminal.write(arguments[0] + " not found.\n")
            }
        }
    },
    write:function(str){
        Terminal.out.innerHTML += str;
    },
    endRunningProcess:function () {
        if(!Terminal.running){
            Terminal.running = null;
            Terminal.timers.forEach(function (t) {
                clearInterval(t);
            });
            Terminal.write("Runing process ended.");
        }

    },
    pop:function () {

    },
    env:{},
    timers:[],
    memory:{},
    commands:{
        chat:chat
    }
};

function chat(args) {
    if(!("color" in Terminal.env)) Terminal.env['color'] = 'white';
    if(!("name" in Terminal.env)) Terminal.env['name'] = 'anonymous';

    Terminal.memory['mq'] = new IsoMQ("isogen.net:8000", args[1]);
    Terminal.memory['mq'].onopen = function () {
        Terminal.write("Connection to '" + args[1] + "' opened!");
    };
    Terminal.memory['mq'].onmessage = function (data) {
        Terminal.write(data);
    };
    Terminal.running = function (line) {
        if("line" == "/exit"){
            Terminal.endRunningProcess();
            return;
        }
        console.log(line);
        Terminal.memory['mq'].send("[<span style='color: "+ Terminal.env['color'] + "'>" + Terminal.env['name'] + "</span>]: " + line);
    }
}

