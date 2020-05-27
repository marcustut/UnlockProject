// require the discord.js module
const Discord = require('discord.js');
const { prefix, token } = require('./config.json');

// create a new Discord Client
const client = new Discord.Client();

// When the client is ready, run this code
// this event will only trigger one time after logging in
client.once('ready', () => {
	console.log('Ready!');
});

client.on('message', message => {
	console.log(message.content);
	if (message.content.startsWith(`${prefix}ping`)) {
		message.channel.send('Pong.');
	} else if (message.content.startsWith(`${prefix}beep`)) {
		message.channel.send('Boop.');
	} else if (message.content === `${prefix}server`) {
		message.channel.send(`This server's name is: ${message.guild.name}`);
	}
});

// login to Discord with the App's Token
client.login(token);