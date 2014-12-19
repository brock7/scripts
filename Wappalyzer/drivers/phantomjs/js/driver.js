(function() {
	var
		url,
		originalUrl,
		args  = [],
		debug = false;

	try {
		require('system').args.forEach(function(arg) {
			switch ( arg ) {
				case '-v':
				case '--verbose':
					debug = true;

					break;
				default:
					url = originalUrl = arg;
			}
		});

		if ( !url ) {
			throw new Error('Usage: phantomjs ' + require('system').args[0] + ' <url>');
		}

		if ( !phantom.injectJs('js/wappalyzer.js') ) {
			throw new Error('Unable to open file js/wappalyzer.js');
		}

		wappalyzer.driver = {
			/**
			 * Log messages to console
			 */
			log: function(args) {
				if ( debug || args.type !== 'debug' ) {
					console.log(args.message);
				}
			},

			/**
			 * Display apps
			 */
			displayApps: function() {
				var
					app,
					apps  = [],
					cats  = [],
					count = wappalyzer.detected[url] ? Object.keys(wappalyzer.detected[url]).length : 0;

				wappalyzer.log('driver.displayApps');

				if ( count ) {
					for ( app in wappalyzer.detected[url] ) {

						wappalyzer.apps[app].cats.forEach(function(cat) {
							cats.push(wappalyzer.categories[cat]);
						});

						apps.push({
							url:         originalUrl,
							finalUrl:    url,
							application: app,
							confidence:  wappalyzer.detected[url][app].confidenceTotal,
							version:     wappalyzer.detected[url][app].version,
							categories:  cats
						});
					}

					console.log(JSON.stringify(apps));
				}
			},

			/**
			 * Initialize
			 */
			init: function() {
				var
					page, hostname,
					headers = {};
					a       = document.createElement('a'),
					json    = JSON.parse(require('fs').read('apps.json'));

				wappalyzer.log('driver.init');

				a.href = url.replace(/#.*$/, '');

				hostname = a.hostname;

				wappalyzer.apps       = json.apps;
				wappalyzer.categories = json.categories;

				page = require('webpage').create();

				page.onConsoleMessage = function(message) {
					wappalyzer.log(message);
				};

				page.onResourceReceived = function(response) {
					if ( response.url.replace(/\/$/, '') === url.replace(/\/$/, '') ) {
						if ( response.redirectURL ) {
							url = response.redirectURL;

							return;
						}

						if ( response.stage === 'end' && response.contentType.indexOf('text/html') !== -1 ) {
							response.headers.forEach(function(header) {
								headers[header.name.toLowerCase()] = header.value;
							});
						}
					}
				};

				page.open(url, function(status) {
					var html, environmentVars;

					if ( status === 'fail' ) {
						return;
					}

					html = page.content;

					if ( html.length > 50000 ) {
						html = html.substring(0, 25000) + html.substring(html.length - 25000, html.length);
					}

					// Collect environment variables
					environmentVars = page.evaluate(function() {
						var i, environmentVars;

						for ( i in window ) {
							environmentVars += i + ' ';
						}

						return environmentVars;
					});

					wappalyzer.log({ message: 'environmentVars: ' + environmentVars });

					environmentVars = environmentVars.split(' ').slice(0, 500);

					wappalyzer.analyze(hostname, url, {
						html:    html,
						headers: headers,
						env:     environmentVars
					});

					phantom.exit();
				});
			}
		};

		wappalyzer.init();
	} catch ( e ) {
		console.error(e);

		phantom.exit();
	}
})();
