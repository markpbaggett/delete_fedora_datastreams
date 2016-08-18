# README

## About

Example code to purge old versions of Fedora datastreams based on parent namespace.

**Warning:** this is in progress.

## Step 1: Create Configuration file

Before using, make a copy of **default_configuration.yaml** and save as **configuration.yaml**.  Complete the following information:

* fedoraurl: This key points at your instance of Fedora.
* username: This is your Fedora username.
* password: This is your Fedora password.
* collection\_namespace: Parent namespace of your collection.
* datastream: The datastream you want to purge.
* start: This purges versions of datasreams based on date range. This value holds the start of the range. Use one of these two formats:
	* yyyy-MM-dd
	* yyyy-MM-ddTHH:mm:ssZ
* end: This purges versions of datasreams based on date range. This value holds the end of the range. Use one of these two formats:
	* yyyy-MM-dd
	* yyyy-MM-ddTHH:mm:ssZ