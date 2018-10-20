<?php
/**
 * Extract text from XML transcript (ASR output)
 *
 * Run as php xml2csv.php -f $file.xml > $output.file to get all sentences
 *
 * -f $file  XML file
 * -s str    output field separator
 * -c float  confidence threshold
 * -d        Print detailed output (start, end, speaker)
 * 
 * @ Evgeny A. Stepanov
 */
error_reporting(E_ALL);
ini_set('memory_limit', -1);
ini_set('display_errors', 1);

// Script arguments
$args = getopt('f:s:c:d');

// Global definitions
$glue = (isset($args['s'])) ? $args['s'] : ',';
$prec = 2; // precision
$conf = (isset($args['c'])) ? $args['c'] : 0.0;

// Logging
$errfh = fopen( 'php://stderr', 'w' );

// Load XML
$xml = new DOMDocument();
$xml->load($args['f']);
$dom_xpath = new DOMXPath($xml);

/*--------------------------------------------------------------------*/
// Get Sentences
$sent_query = '//sentence';
$sent_nlist = $dom_xpath->query($sent_query);

foreach ($sent_nlist as $sent_node) {
	$sb = $sent_node->getAttribute('start');     // time begin
	$se = $sent_node->getAttribute('end');       // time end
	$ss = $sent_node->getAttribute('speakerID'); // speaker ID
	
	// get words
	$word_query = './item';
	$word_nlist = $dom_xpath->query($word_query, $sent_node);
	
	$word_array = array();
	$conf_array = array();
	
	foreach ($word_nlist as $word_node) {
		$word_array[] = $word_node->nodeValue;
		$conf_array[] = $word_node->getAttribute('conf');
	}
	
	// average confidence
	if (empty($word_array)) {
		$sent_conf = number_format(0, $prec);
	}
	else {
		$sent_conf = number_format(round(array_sum($conf_array)/count($conf_array), $prec), $prec);
	}
	
	if ($sent_conf >= $conf) {
		if (isset($args['d'])) {
			echo implode($glue, array($ss, $sb, $se, $sent_conf)) . $glue;
			
		}
		echo implode(' ', $word_array) . "\n";
	}
}

fclose($errfh);
