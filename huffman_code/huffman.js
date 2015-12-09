function frequency(str){
	var freqs={};
        len=str.length;
	for(var ch=0;ch<len;ch++){
		if (str[ch] in freqs){	
			freqs[str[ch]]+=1;
			}
		else{
			freqs[str[ch]]=1;
			}
		}
	return freqs;
	}


function sortfreq(freqs){
	var letters=Object.keys(freqs);
	var tuples=[];
	var len=letters.length
	for(var i=0;i<len;i++){
		var le=letters[i]
		var n=[];
                n.push(freqs[le],le);
		tuples.push(n);
	 			
		}
	tuples.sort(function(a,b){
	    	retVal=0;
    		if(a[0]!=b[0]) retVal=a[0]>b[0]?1:-1;
	    	else if(a[1]!=b[1]) retVal=a[1]>b[1]?1:-1;		
    		return retVal
	});
	return tuples;
	}




function buildtree(tuples){
	while(tuples.length>1){
		var leasttwo=tuples.slice(0,2);
		var therest=tuples.slice(2,tuples.length);
		var combfreq = leasttwo[0][0] + leasttwo[1][0];
		var c=[combfreq,leasttwo];
		therest.push(c);
		tuples=therest;
		tuples.sort(function(a,b){
   		    var retVal=0,i=0;
		    if(a[0]!=b[0]) retVal=a[0]>b[0]?1:-1;
		    else if(a[1].length!=b[1].length) retVal=a[1].length>b[1].length?1:-1;
		    return retVal;
		    });
//		console.log(tuples);
		}
	return tuples[0]          	
	}



function trimTree(tree){
	var p = tree[1];
//	console.log('p is',p);
	if (typeof p == 'string'){
		return p;
	}	
	else{
		return [trimTree(p[0]), trimTree(p[1])];
		
	}
	}	


var codes={};
function assigncode(node,pat){
	 pat = pat || "";
//	console.log(node,pat);		
	if (typeof(node)=='string'){
		codes[node]=pat;
//		console.log(codes);
	}
	else {
		assigncode(node[0], pat+"0") ;
        	assigncode(node[1], pat+'1');
		}
//	return codes
	}



function encode (str) {
    var output = "";
     len=str.length;
        for(var ch=0;ch<len;ch++){
             output+=codes[ str[ch]];
	}
    return output
}

function showCodes(){
console.log(codes);
	}


function decode(tree,str){
   var output="";
   var p=tree;
   for (var i=0;i<str.length;i++){
       if(str[i] == '0'){
           p=p[0];
           }
       else{
           p=p[1];
       }
       if (typeof p === 'string'){
           output = output +p;
           p=tree;
           }
   }
   return  output;
}



function main(){
var debug = 1;
str= "aa yzabccdeeeeeffg"
freqs = frequency(str);
tuples = sortfreq(freqs);
tree = buildtree(tuples);
   if (debug){
console.log("Built tree" , tree);
}
   tree = trimTree(tree);
   if (debug){
console.log("Trimmed tree", tree);
}
   assigncode(tree);
   if (debug){
showCodes();
}
small = encode(str);
original = decode (tree, small);
console.log("Original text length"+ str.length);
   //console.log("Requires %d bits. (%d bytes)" % ((small.length), (small.length+7)/8);
console.log("Restored matches original:");
if(str === original){
console.log("Yes");
}
else{
console.log("No");
}
   console.log("Code for space is "+ codes[' ']);
   console.log("Code for letter e "+ codes['e']);
   console.log("Code for letter y "+ codes['y']);
   console.log("Code for letter z "+ codes['z']);

}
main();


/*
var f="aaabccdeeeeeffg";
fr=frequency(f);
t=sortfreq(fr);
te=buildtree(t);

//console.log(te);
tr=trimTree(te);
//console.log(tr);
c=assigncode(tr);
//console.log(c);
e=encode(f);
console.log(e);*/
