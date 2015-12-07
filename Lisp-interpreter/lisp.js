
var tokenize=function (program){
   

   return program.replace(/\(/g,'( ').replace(/\)/g,' )').split(/ +/);
}





function read_from_tokens(list){
    
    if (list.length===0){
       throw "unexpected EOF"
    }
    token=list.shift()
    if (token==='('){
         var L=[];
         while(list[0] !== ')' ){
                L.push(read_from_tokens(list));
                }
         list.shift();
         return L;
    }
    else if (token===')'){
          throw "invalid."
    }
    else{
       r=atom(token);
       return r;
    }

}





function atom(token){
    if (isNaN(parseInt(token))){
      return token;
    }   
     else if(token.indexOf('.')!==-1){
       return parseFloat(token);
   }
   else{
      return parseInt(token);
  }
}




var parse=function (program){
   
   return read_from_tokens(tokenize(program));
   
}





function add(){
   return arguments[0]+arguments[1];
   }

function sub(){
   return arguments[0]-arguments[1];
   }
function mul(){
   return arguments[0]*arguments[1];
   }
function div(){
   if (arguments[1]==0){
      throw "Division by zero is undefined";
   }
   return arguments[0]/arguments[1];
   }
function gt(){
	return arguments[0]>arguments[1];
	}
function lt(){
        return arguments[0]<arguments[1];
        }
function ge(){
        return arguments[0]>=arguments[1];
        }
function le(){
        return arguments[0]<=arguments[1];
        }
function eq(){
        return arguments[0]==arguments[1];
        }
function abs(){
	return Math.abs(arguments[0]);
	}
function apply(){
	 arguments[0].apply(this, arguments[1]);
	}
function begin(op1){
	return op1[op1.length-1];
        }
function len(op1){
	return op1.length;
	}
function car(op1){
	return op1[0];
	}
function cdr(op1){
	return op1.slice(1,op1.length);
	}

function Env(parms, args, outer) {
    var i = 0;
    for (i = 0; i < parms.length; i++){

        this[parms[i]] = args[i];
 	}
    this.outer = outer;
    this.find = function(variable) {
        if (variable in this) {	 
            return this;
        }
        else {
            var p = this.outer.find(variable);
            return p;
        }
    };
}
var global_env = standard_env();
var procedure = function(params, body, env) {
    this.params= params;
    this.body = body;
    this.env = env;
    this.execute = function(args) {
	o= new Env(this.params, args, this.env)
        return evalu(this.body,o);
    };
};
	
function standard_env(){
   	var env= new Env([], [], null);
        env['+']=add;
 	env['-']=sub, 
	env['*']=mul;
	env['/']=div,
        env['>']=gt;
	env['<']=lt;
	env['>=']=ge;
	env['<=']=le;
	env['=']=eq;
        env['abs']=abs;
	env['append']=add;
	env['apply']=apply;
        env['begin']=begin;
	env['length']=len;
	env['car']=car;
	env['cdr']=cdr;
        return env;
    }

env=global_env;


function evalu(x,env){
        
  	
        if (typeof(x)=='string'){
            
		var y=env.find(x)[x];
          
                return y;
	}
        else if (typeof(x)=='number'){
		return x;
        }
        else if(x[0] == 'quote') {
		return x[1];
	}
	else if(x[0] == 'if') {
		test = x[1];
		conseq = x[2];
		alt = x[3];
               
		if(evalu(test,env))
			return evalu(conseq,env);
		else
			return evalu(alt,env);
	}
	else if(x[0] == 'define') {
		variable = x[1];
		expr = x[2];
		env[x[1]] = evalu(expr,env);
                return ;
	}	
	else if(x[0]=='set!'){
                variable=x[1];
                expr=x[2];
                env[variable]=evalu(expr,env);

                return env[variable];
		}
	else if (x[0] === 'lambda') {
        var parms = x[1];
        var body = x[2];
        var p=new procedure(parms, body, env);
        return p
    }
        else {
               var proc=evalu(x[0],env);             
             
        	var args=[];
	        for (var i = 1, count=x.length;i<count;i++){
                        var v=evalu(x[i],env);
                    	args.push(v);
		}
		if (proc instanceof procedure) {
            
	            return proc.execute(args);
        		}
        	return  proc.apply(this,args);
 	}
}


function eval(p){
	return evalu(p,env);
}	


/*var program="(define r 10) ";
console.log(parse(program));
r=eval(parse(program))
console.log("eval is",eval(parse("(* r r )")));
console.log(eval(parse("(set! r (* r r))")));
console.log(eval(parse("(* r r )")));
program="(begin (quote ( 2 3 5 6 )))";
console.log("eval is",eval(parse(program)));
program="(cdr (quote (1 2 3)))"
console.log(parse(program));
console.log("eval is",eval(parse(program)));
var  p="(define sqr (lambda (r) (* r r)))"

console.log("define eval is",eval(parse(p)));
console.log(eval(parse("(sqr 9)")));*/

p="(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))"

eval(parse(p));
console.log(eval(parse("(fact 4)")));


//var p="(if (<= 5 1) 1 (+ 5 4))"
//console.log(eval(parse(p)));


