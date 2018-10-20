<?php
/***
 * Convert exb xml to csv 
 * 
 * Run as php exb2csv.php -f $file.xml > $output.file to get all sentences
 *
 * -f $file  XML file
 * -s str    output field separator
 * -c float  confidence throshold
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
$junk = array('SILENCE', 'Silence');

// Logging
$errfh = fopen( 'php://stderr', 'w' );

// Load XML
$xml = new DOMDocument();
$xml->load($args['f']);
$dom_xpath = new DOMXPath($xml);

$dom_xpath->registerNamespace('php', 'http://php.net/xpath');
$dom_xpath->registerPhpFunctions(); // Allow all PHP functions

/*--------------------------------------------------------------------*/
// Get Speakers
$spk_query = '//head/speakertable/speaker[@id]';
$spk_nlist = $dom_xpath->query($spk_query);
$spk_array = array();
foreach ($spk_nlist as $spk_node) {
	// ID as attribute
	$spk_array[] = $spk_node->getAttribute('id');
}

// Timeline
$time_query = '//common-timeline/tli';
$time_nlist = $dom_xpath->query($time_query);
$time_array = array();
foreach ($time_nlist as $time_node) {
	$time_id   = $time_node->getAttribute('id');
	$time_time = $time_node->getAttribute('time');
	$time_array[trim($time_id)] = trim($time_time);
}

// Transcriptions
$trs_query = "//tier[@type='t' and @category='asr_transcription']";
$trs_nlist = $dom_xpath->query($trs_query);
$trs_array = array();
foreach ($trs_nlist as $trs_node) {
	// tier ID
	$tier_id = $trs_node->getAttribute('id');
	// Speaker
	$spk_id	 = trim($trs_node->getAttribute('speaker'));
	
	// events
	$event_query = './event';
	$event_nlist = $dom_xpath->query($event_query, $trs_node);
	foreach ($event_nlist as $event_node) {
		$es = $event_node->getAttribute('start');
		$ee = $event_node->getAttribute('end');
		$el = $event_node->getAttribute('LikelihoodPerFrame');
		
		// Access text() node directly [to avoid issues]
		$txt_query = './text()';
		$txt_nlist = $dom_xpath->query($txt_query, $event_node);
		$txt_array = array();
		foreach ($txt_nlist as $txt_node) {
			$txt_array[] = trim($txt_node->nodeValue);
		}
		$txt = implode(' ', $txt_array);
		
		$event = array(
				'es'	=> $es, //$time_array[$es],
				'ee'	=> $ee, //$time_array[$ee],
				'el'    => number_format(floatval($el), $prec),
				'spk'	=> $spk_id,
				'txt'	=> trim($txt), 
		);
		
		$trs_array[] = $event;
	}
}

/***
 * OUTPUT
 */
foreach ($time_array as $k => $time) {
	$event = get_subarray_by_keyval($trs_array, 'es', $k);
		
	if ($event['txt'] != '' && !in_array($event['txt'], $junk)) {
		if ($event['el'] >= $conf) {
			if (isset($args['d'])) {
				$tmp_arr = array();
				$tmp_arr[] = $event['spk'];
				$tmp_arr[] = $time_array[$event['es']];
				$tmp_arr[] = $time_array[$event['ee']];
				$tmp_arr[] = $event['el'];
				echo implode($glue, $tmp_arr) . $glue;
			}
			echo $event['txt'] . "\n";
		}
	}
}

fclose($errfh);

/***
 * FUNCTIONS
 */

/**
 * Get sub array by key and value of one of its elements
 * @param 	array 	$arr
 * @param 	string 	$key
 * @return 	mixed 	$val
 */
function get_subarray_by_keyval($arr, $key, $val) {
	foreach ($arr as $e) {
		if ($e[$key] == $val) {
			return $e;
		}
	}
}
