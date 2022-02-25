/*---------------------------------------------------------------------------------------------------------------
 ChroPro

pour remplacer serial-port-json-server, utiliser nodeJS portable avec le module nodeSerial et développer un script serveur équivalent :
https://serialport.io/docs/en/api-stream
https://itp.nyu.edu/physcomp/labs/labs-serial-communication/lab-serial-communication-with-node-js/
https://github.com/milochen0418/nodejs-websocket-to-serialport/commit/24b41827a2a27b487664fbd34bb33cff95d77eb5 
---------------------------------------------------------------------------------------------------------------*/


// Charger le contenu de ce script seulement si Session ChroPro
if(sessionStorage.getItem("chropro") == "true")
{

//#######################################################################################################################################################
// Ouverture d'indexedDB en tout PREMIER pour pouvoir logger dedans !!!!
var db;

// exemple de tableau de données
const customerData = [
  { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
  { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
];

// ouverture de la bdd
var request = indexedDB.open('bdd_ChroPro', 6);	// une changement de version déclenche l'évènement onUpgradeNeeded 

request.onerror = function(event) {
  alert("IndexedDB non autorisée ou impossible à upgrader, veuiller effacer la bdd");
  console.log('IndexedDB non autorisée ou impossible à upgrader, veuiller effacer la bdd');
};

request.onsuccess = function(event) {
	db = event.target.result;
};

// onupgradeneeded est le seul endroit où vous pouvez modifier la structure de la base de données. Dans cette méthode, vous pouvez créer et supprimer des objets de stockage, construire et supprimer des index.
request.onupgradeneeded = function(event) {
	db = event.target.result;

  // Créer un objet de stockage qui contient les informations de nos clients. 
  // Nous allons utiliser "ssn" en tant que clé parce qu'il est garanti d'être 
  // unique - du moins, c'est ce qu'on en disait au lancement.
  var objectStore = db.createObjectStore("log", { autoIncrement : true });

  // Créer un index pour rechercher les clients par leur nom. Nous pourrions 
  // avoir des doublons (homonymes), alors on n'utilise pas d'index unique.
  objectStore.createIndex("name", "name", { unique: false });

  // Créer un index pour rechercher les clients par leur adresse courriel. Nous voulons nous
  // assurer que deux clients n'auront pas la même, donc nous utilisons un index unique.
  objectStore.createIndex("email", "email", { unique: true });

  // Utiliser la transaction "oncomplete" pour être sûr que la création de l'objet de stockage
  // est terminée avant d'ajouter des données dedans.
  objectStore.transaction.oncomplete = function(event) {
	// Stocker les valeurs dans le nouvel objet de stockage.
	var logObjectStore = db.transaction("log", "readwrite").objectStore("log");
	logObjectStore.add("initialisation de la bdd");
  }
};


//#######################################################################################################################################################
// Gestion des logs
function log(message)
{
	try{
		if (message.substr(2, 1) == ':' && message.substr(5, 1) == ':') // ne pas afficher l'heure si elle est déjà contenue dans le message
		{
			// afficher dans la console
			console.log(message);
			// afficher au journal
			document.getElementById('sas').innerHTML += message + "<br>";
			// envoyer au fichier log.txt via WebSocket et SerialPortServer -verbose
			//monSocket.send("¤" + message + "¤"); 
			// stocker dans indexedDB
			var logObjectStore = db.transaction("log", "readwrite").objectStore("log");
			logObjectStore.add(message);
		}else{
			// afficher dans la console
			console.log(heure() + " - " + message);
			// afficher au journal
			document.getElementById('sas').innerHTML += heure() + " - " + message + "<br>";
			// envoyer au fichier log.txt via WebSocket et SerialPortServer -verbose
			//monSocket.send("¤" + heure() + " - " + message + "¤"); 
			// stocker dans indexedDB
			var logObjectStore = db.transaction("log", "readwrite").objectStore("log");
			logObjectStore.add(heure() + " - " + message);
		}
	}catch(e) {console.log("erreur fonction log")}
} // fin logs

log('PYZ');


//#######################################################################################################################################################
// Afficher le DIV HTML
var e=document.createElement("div");
e.setAttribute("id", "emplacementChroPro");
//e.setAttribute("style", "float:left; top:0; left:0; width:250px; height:100%; background-color:#DCCCDC;");
e.setAttribute("style", "float:right; top:0; right:0; width:250px; height:100%; background-color:#DCCCDC;");
//document.body.appendChild(e);
document.body.prepend(e);

document.getElementById('emplacementChroPro').innerHTML = '\
<div id="Moniteur" style="border:solid; width:150px; background-color:white; font-size: 30px; font-family: Monaco, monospace; text-align: center; margin: auto;">Afficheur</div>\
<input id="inverserCellules" type="checkbox" ' + sessionStorage.inverserCellules + ' onclick="inverserCellules(this);"/>Inverser Départ/Arrivée<br>\
<input type="button" onClick="reco();" value="Reco">\
<input type="number" id="tempsReco" min="1" max="60" value="5" style="width:60px">\
<input type="button" onClick="finReco();" value="Fin">\
<br><a href="chropro_log.htm" target="_blank">Logs</a>\
<div id="sas"></div>\
';

log('PYZ2');


//#######################################################################################################################################################
// éxcéuter après le chargement de la page :
if(window.addEventListener){
    window.addEventListener('load', apresPage, false);
}else{
    window.attachEvent('onload', apresPage);
}


function apresPage(){

	// Intercepter les appuis sur les boutons
	document.getElementById("boutonDepart").addEventListener("click", departManuel);
	document.getElementById("boutonArrivee").addEventListener("click", arriveeManuel);
	document.getElementById("boutonReset").addEventListener("click", raz);
	document.getElementById("boutonFaute").addEventListener("click", afficherFautes);
	document.getElementById("boutonFauteMoins").addEventListener("click", afficherFautes);
	document.getElementById("boutonRefus").addEventListener("click", afficherFautes);
	document.getElementById("boutonRefusMoins").addEventListener("click", afficherFautes);
	document.getElementById("E").addEventListener("click", afficherMention);
	
	// afficher le concourrent dans les log
	log(document.getElementById('dossard').value
	+ " - " + document.getElementById('nomChien').innerText
	+ " - " + document.getElementById('nomConducteur').innerText
	+ " - " + document.getElementById('nomEpreuve').innerText
	+ " - " + document.getElementById('nomCategorie').innerText
	+ " - " + document.getElementById('nomClasse').innerText
	);

	// au chargement de la page, initialiser le chrono, sauf si départ en cours
	if(sessionStorage.etat != 'depart' && sessionStorage.mode != 'reco') {raz();}

} //fonction aprespage



//#######################################################################################################################################################
// Reco

var timerIDreco = null;

function reco() {
	sessionStorage.mode = 'reco';
	startReco = new Date();
	startReco.setMinutes( startReco.getMinutes() + document.getElementById('tempsReco').value*1);
	sessionStorage.startReco = startReco;
	afficherReco();
	clearInterval(timerIDreco);
	timerIDreco = setInterval("afficherReco()", 1000);
}

function afficherReco(){
	try {envoyer("<EW");}catch(e){}	//arrêter l'affichage chrono boitier en définissant un état bidon 
	clearInterval(defilantID);	//arrêter le dossard défilant
	var end = new Date();
	var diff = startReco - end;
	diff = new Date(diff);
	var sec = diff.getSeconds();
	var min = diff.getMinutes();
	if (min < 10){
		min = "0" + min;
	}
	if (sec < 10){
		sec = "0" + sec;
	}
	afficher( min + "m" + sec + "s" );
	if(diff <= 0) finReco();
}

function finReco() {
	clearInterval(timerIDreco);
	timerIDreco = null;
	sessionStorage.startReco = 0;
	sessionStorage.mode = '';
	raz();
}

// continuer une reco auchargement de la page
if (sessionStorage.startReco != 0) {
	startReco = new Date(sessionStorage.startReco);
	afficherReco(); 
	timerIDreco = setInterval("afficherReco()", 1000);
}


//#######################################################################################################################################################
// Ouverture Websocket pour communication avec le serveur serial-port-json-server : https://github.com/johnlauer/serial-port-json-server

var	monSocket = new WebSocket("ws://localhost:8989/ws");

// Déclaration variables globales
var portChroPro;
var bufferChroPro;
//var sessionStorage.etat;
var marque = sessionStorage.getItem("marque");
var mot = []; // c'est un objet pas un tableau
adopterLexique();
var defilantID;
var positionDefilement;


monSocket.onopen =  function (event)
{
	log('WebSocket ouvert.');
	detecterPorts();
}

monSocket.onclose =  function (event)
{
	log('WebSocket fermé. Vérifier que SerialPortJSONserver.exe est lancé.');
}

monSocket.onerror =  function (event)
{
	log('Erreur Websocket.');
}

function detecterPorts()
{
	monSocket.send("list"); 
}

function ouvrirPort(port)
{
	monSocket.send("open " + port + " 9600 default");	// ouvrir port COM
}

function envoyer(trame)
{
	monSocket.send("send "+portChroPro+" "+trame); 
}

function fermerPort()
{
	monSocket.send("close "+portChroPro); 

}

monSocket.onmessage = function (event)
{
  //console.log("RECU : " + event.data);
  try {var msg = JSON.parse(event.data);} // tester si message  JSON
  catch(e) {return}
	  // si ouverture
	  if (msg.Cmd == "Open")
	  {
		  log("Port "+msg.Port+" ouvert.");
	  }
	  
	  // si echec ouverture
	  if (msg.Cmd == "OpenFail")
	  {
		  log("Impossible d'ouvrir le port "+msg.Port+" ou port déjà ouvert. Redémarrer ChroPro.");
	  }
	  
	  if (msg.Msg == "demanderLog")
	  {
		  log("Demande de téléchargement des logs");
			var objectStore = db.transaction("log").objectStore("log");
			var bufferLog;
			   
			   objectStore.openCursor().onsuccess = function(event) {
				  var cursor = event.target.result;
				  
				  if (cursor) {
					 bufferLog += cursor.value + "<br>";
					 cursor.continue();
				  } else {
					 monSocket.send(bufferLog);
					 monSocket.send("FIN_LOG");
				  }
			   };
	  }

	  // Intercepter port COM
	  if (msg.SerialPorts)
	  {
		  //log(msg.SerialPorts)
		  msg.SerialPorts.forEach(function(p) {
			  // Duemilanove || Uno AT16U2 || Uno CH340
			  if ((p.UsbVid == "0403" && p.UsbPid == "6001") || (p.UsbVid == "2341" && p.UsbPid == "0043") || (p.UsbVid == "1A86" && p.UsbPid == "7523") || (p.UsbVid == "10C4" && p.UsbPid == "EA60"))
			  {
				  portChroPro = p.Name;
				  log("Port détecté : "+ portChroPro);
				  if (p.IsOpen)
				  {
					  log("Port " + portChroPro + " déjà ouvert")
				  }else{
					  ouvrirPort(portChroPro);
				  }
			  }
		  });
	  }
	  
	  // si message reçu
	  if (msg.P == portChroPro && msg.D)
	  {
		  bufferChroPro += msg.D;		//agréger le buffer
		  //console.log("BUFFER : "+bufferChroPro);
		  
		  // Intercepter marque du boitier :
		  var debutTrameMarque = bufferChroPro.indexOf("{");		// position du caractére annonçant le début de la trame
		  if (debutTrameMarque != -1 && bufferChroPro.length > debutTrameMarque+1)
		  {
			  marque = bufferChroPro.substr(debutTrameMarque+1, 1);
			  sessionStorage.setItem("marque",marque);
			  adopterLexique();
			  log("Marque boitier : " + mot['Marque']);
			  bufferChroPro = bufferChroPro.slice(debutTrameMarque+2);	//vider le buffer déjà lu
		  }

		  // Intercepter trames de départ :
		  var debutTrameDepart = bufferChroPro.indexOf("[D");		// position du caractére annonçant le début de la trame
		  var finTrameDepart = bufferChroPro.indexOf("D]");		// position du caractére annonçant le début de la trame
		  if (debutTrameDepart != -1 && finTrameDepart != -1)
		  {
			  var heureDepart = bufferChroPro.substring(debutTrameDepart+2, finTrameDepart);
			  //log("TRAME de départ : " + heure(ArduinoToDate(heureDepart)));
			  bufferChroPro = bufferChroPro.slice(finTrameDepart+3);	//vider le buffer déjà lu
			  depart(ArduinoToDate(heureDepart));
		  }

		  // Intercepter trames de arrivée :
		  var debutTrameArrivee = bufferChroPro.indexOf("[A");		// position du caractére annonçant le début de la trame
		  var finTrameArrivee = bufferChroPro.indexOf("A]");		// position du caractére annonçant le début de la trame
		  if (debutTrameArrivee != -1 && finTrameArrivee != -1)
		  {
			  var heureArrivee = bufferChroPro.substring(debutTrameArrivee+2, finTrameArrivee);
			  //log("TRAME d'arrivée : " + heure(ArduinoToDate(heureArrivee)));
			  bufferChroPro = bufferChroPro.slice(finTrameArrivee+3);	//vider le buffer déjà lu
			  arrivee(ArduinoToDate(heureArrivee));
		  }
		  
		  // Intercepter trames dédiées a l'afficheur :
		  var debutTrameAfficheur = bufferChroPro.indexOf(String.fromCharCode(02));		// position du caractére annonçant le début de la trame
		  var finTrameAfficheur = bufferChroPro.indexOf(String.fromCharCode(10), debutTrameAfficheur+1);		// position du caractére annonçant la fin de la trame
		  if (debutTrameAfficheur != -1 && finTrameAfficheur != -1)
		  {
			  var moniteur = bufferChroPro.substring(debutTrameAfficheur, finTrameAfficheur);
			  moniteur = moniteur.replace(String.fromCharCode(02)+'13', '');	// debut de trame Tag Heuer
			  moniteur = moniteur.replace(/[?]/g, '');	// trame Microgate
			  moniteur = moniteur.replace(String.fromCharCode(02), '');
			  moniteur = moniteur.replace(String.fromCharCode(10), '');
			  moniteur = moniteur.replace(String.fromCharCode(13), '');
			  moniteur = moniteur.replace(/[ ]/g, ' ');	// caractère invisible ALT+255 sinon les espace multiple ne s'affichent pas en HTML dans le texte défilant
			  document.getElementById('Moniteur').innerHTML = moniteur;
			  bufferChroPro = bufferChroPro.slice(finTrameAfficheur+1);	//vider le buffer déjà lu
		  }
		  
	  } //message reçu

}


//#######################################################################################################################################################
// Fonctions du chrono

function raz()
{
	synchro();
	envoyer("<ER");
	sessionStorage.etat = 'ready';
	fautes = 0;
	refus = 0;
	mention = '';
	positionDefilement = 0;
	var message  = " " + document.getElementById('dossard').value + " - " + document.getElementById('nomChien').innerText + " - " + document.getElementById('nomConducteur').innerText;
	//afficher(message);
	clearInterval(defilantID);
	defilantID = setInterval(function() {defilement(message)}, 200);
	log("reset");
}

function departManuel()
{
	var d = new Date();
	envoyer("<D"+dateToArduino(d));
	depart(d, 'manuel'); 
}

function depart(date, manuel = '')
{
	if (sessionStorage.etat == 'ready')
	{
		clearInterval(defilantID);	//arrêter le dossard défilant
		horaireDepart = date;
		log(heure(date) + " - DEPART " + manuel);
		sessionStorage.etat = 'depart';
		startChronoJS();
	}else{
		log(heure(date) + " - Autre départ " + manuel);
	}
}

function arriveeManuel()
{
	var d = new Date();
	envoyer("<A"+dateToArduino(d));
	arrivee(d, 'manuelle'); 
}

function arrivee(date, manuel = '')
{
	if (sessionStorage.etat == 'depart')
	{
		horaireArrivee = date;
		log(heure(date) + " - ARRIVEE " + manuel);
		var temps = (horaireArrivee - horaireDepart) / 1000;
		temps = temps.toFixed(2);
		stopChronoJS();
		document.getElementById('tempsChrono').value = temps	// écraser l'estimation du temps 
		log("Temps = " + temps);
		sessionStorage.etat = 'arrivee';
	}else{
		log(heure(date) + " - Autre arrivee " + manuel);
	}
}

function afficherFautes()
{
	var fautes = document.getElementById('fautes').value*1 + document.getElementById('refus').value*1
	if (fautes > 9) fautes = 9;
	log(heure() + " - FAUTES : " + fautes);
	envoyer("<F"+fautes); 
}

// Afficher la mention éliminé ou abandon
function afficherMention()
{
	if (document.getElementById('E').value == 'X')
	{
		sessionStorage.etat = 'pause';
		envoyer("<EP");
		afficher(mot['Elimine']);
		log(heure()+" - ELIMINE");
	}else{
		sessionStorage.etat = 'depart';
		envoyer("<ED");
		log(heure()+" - EN COURSE");
	}
}

function inverserCellules(objet)
{
	if(objet.checked == true)
	{
		sessionStorage.inverserCellules = 'checked';
		envoyer("<I1");
	}else{
		sessionStorage.inverserCellules = '';
		envoyer("<I0");
	}
}

// Synchro d'horloge avec le boitier
function synchro()
{
	d = new Date();
	envoyer("<S"+dateToArduino(d)); 
}

// Création du temps sous forme de 4 caractères décimaux
function dateToArduino(date)
{
	var hr = date.getHours();
	var m = date.getMinutes();
	var sec = date.getSeconds();
	var ms = date.getMilliseconds();
	var centiemes = ms.toString().substring(0,2);
	return String.fromCharCode(hr)+String.fromCharCode(m)+String.fromCharCode(sec)+String.fromCharCode(centiemes);
}

// Conversion du timestamp Arduino en date
function ArduinoToDate(horaireArduino)
{
	var heures = Math.floor(horaireArduino / 100/3600);
	var minutes = Math.floor((horaireArduino/100)%3600 / 60);
	var secondes = Math.floor((horaireArduino % 6000)/100);
	var centiemes = horaireArduino % 100;
	
	var d = new Date();
	d.setHours(heures, minutes, secondes, centiemes*10);
	return d;
}

// Formattage de l'heure
function heure(date)
{
	if (date === undefined) {
		var d = new Date();		// heure actuelle
	}else{
		var d = new Date(date);	// heure postée
	}
	var centiemes = d.getMilliseconds().toString().substring(0,2);
	return d.toLocaleTimeString() + "," + centiemes;
}

function adopterLexique()
{

		if 		(marque == "A")	{
								
								mot["Marque"] 	= 	"Alge"; 
								mot["DossardAv"]=	"-";
								mot["DossardAp"]=	" -";
								mot["Elimine"]	=	"  Elin"; 
								mot["Abandon"]	=	" Abond"; 
								}
		else if	(marque == "T")	{
								mot["Marque"]	= 	"Tag Heuer";
								mot["DossardAv"]=	"Doss.";
								mot["DossardAp"]=	"";
								mot["Elimine"]	=	" ELIMINE"; 
								mot["Abandon"]	=	" ABANDON"; 
								}
		else if	(marque == "X")	{
								mot["Marque"]	=	"Xbee";
								mot["DossardAv"]=	"Doss.";
								mot["DossardAp"]=	"";
								mot["Elimine"]	=	" ELIMINE"; 
								mot["Abandon"]	=	" ABANDON"; 
								}
		else if	(marque == "M")	{
								mot["Marque"] 	= 	"MicroGate";
								mot["DossardAv"]=	"-";
								mot["DossardAp"]=	"-";
								mot["Elimine"]	=	"ELIMINE"; 
								mot["Abandon"]	=	"ABANDON"; 
								}
		else if	(marque == "O")	{
								mot["Marque"] 	= 	"Modulo";
								mot["DossardAv"]=	"-";
								mot["DossardAp"]=	"-";
								mot["Elimine"]	=	"ELIMIN"; 
								mot["Abandon"]	=	"ABANDO"; 
								}
}

function defilement(msg)
{
		msg = "    " + msg;
		var defilant = msg.substring(positionDefilement,msg.length) + msg.substring(0,positionDefilement);
		afficher(defilant);
        positionDefilement = (positionDefilement + 1)% msg.length;
}

// Afficher 1ère ligne
function afficher(message)
{
	var message = message.replace(/[ÈÉÊËèéêë]/g, 'E').replace(/[Çç]/g, 'C').replace(/[ÀÁÂÃÄÅàâä]/g, 'A').replace(/[ÌÍÎÏïî]/g, 'I').replace(/[ÙÚÛÜûùü]/g, 'U').replace(/[ÒÓÔÕÖôöó]/g, 'O');
	if (marque == 'T' || marque == 'X')
	{
		// si message trop court, compléter jusqu'à 8 caractères
		message = message.padStart(8);
		// si message trop long, couper à 8 caractères
		message = message.substring(0,8);
		// fabriquer la trame complète 'chr(02)."13".$trame.chr(10)' -> ligne 1, luminosité 3
		var trame = String.fromCharCode(02) + '13' + message + String.fromCharCode(10);
		envoyer(trame);
	}
	
	//supprimer les accents
	/*
	$remplacements = array('Á'=>'A','À'=>'A','Â'=>'A','Ä'=>'A','Ã'=>'A','Å'=>'A','Ç'=>'C','É'=>'E','È'=>'E','Ê'=>'E','Ë'=>'E','Í'=>'I','Ï'=>'I','Î'=>'I','Ì'=>'I','Ñ'=>'N','Ó'=>'O','Ò'=>'O','Ô'=>'O','Ö'=>'O','Õ'=>'O','Ú'=>'U','Ù'=>'U','Û'=>'U','Ü'=>'U','Ý'=>'Y','á'=>'a','à'=>'a','â'=>'a','ä'=>'a','ã'=>'a','å'=>'a','ç'=>'c','é'=>'e','è'=>'e','ê'=>'e','ë'=>'e','í'=>'i','ì'=>'i','î'=>'i','ï'=>'i','ñ'=>'n','ó'=>'o','ò'=>'o','ô'=>'o','ö'=>'o','õ'=>'o','ú'=>'u','ù'=>'u','û'=>'u','ü'=>'u','ý'=>'y','ÿ'=>'y');
	$message = strtr($message, $remplacements);

	// Fabrication trame ALGE
	if ($GLOBALS['marque'] == 'A')
	{
		// si message trop court, compléter jusqu'à 6 caractères
		$message =  str_pad($message, 6, ' ', STR_PAD_LEFT);  
		// convertir le message en '00:00:00' 
		$message = substr($message, 0, 2).':'.substr($message, 2, 2).':'.substr($message, 4, 2);
		// fabriquer la trame complète 'CrCrCrCrCrCr        00:00:00 CR'
		$trame = chr(13).chr(13).chr(13).chr(13).chr(13).chr(13).chr(02)."       ".$message." ".chr(13);
	}

	// Fabrication trame TAG HEUER
	if ($GLOBALS['marque'] == 'T' or $GLOBALS['marque'] == 'X')
	{
		// si message trop court, compléter jusqu'à 8 caractères
		$message =  str_pad($message, 8, ' ', STR_PAD_RIGHT);  
		// si message trop long, couper à 8 caractères
		$message = substr($message, 0, 8);
		// fabriquer la trame complète 'chr(02)."13".$trame.chr(10)' -> ligne 1, luminosité 3
		$trame = chr(02)."13".$message.chr(10);
	}
	
	// Fabrication trame MODULO
	if ($GLOBALS['marque'] == 'O')
	{
		// si message trop court, compléter jusqu'à 8 caractères
		$message =  str_pad($message, 6, ' ', STR_PAD_LEFT);  
		// si message trop long, couper à 8 caractères
		$message = substr($message, 0, 6);
		// fabriquer la trame complète 'chr(02)."13".$trame.chr(10)' -> ligne 1, luminosité 3
		$trame = chr(02)."13".$message.chr(10);
	}
	
	// Fabrication trame MicroGate
	if ($GLOBALS['marque'] == 'M')
	{
		// si message trop court, compléter jusqu'à 7 caractères
		$message =  str_pad($message, 7, ' ', STR_PAD_RIGHT);  
		// si message trop long, couper à 7 caractères
		$message = substr($message, 0, 7);
		// fabriquer la trame complète
		$trame .= chr(02).chr(13)."   ?????????".$message.chr(13);
	}
	
	//envoyer à l'afficheur
	@fwrite($GLOBALS['flux'], $trame);
	// partager le message avec d'autres pages
	//@session_start();
	//$_SESSION['moniteur'] = $message;
	// ecrire les variables de session
	//session_write_close();
*/
}



} // if Session ChroPro