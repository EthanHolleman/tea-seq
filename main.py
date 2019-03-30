#!/usr/bin/python
'''
Title: Main pipeline wrapper for TEA-seq (main.py)
Author: Jasen M. Jackson, '19
Date: 2/20/19-
This script contains the main workflow for the TEA-seq pipeline.
'''
import numpy as np
#import pylab as py
import glob, os
import os.path
import sys
from HL2_params import *
from library_filter import *

def validate_parameters():

	# check that the length of the fastq file lists are all equal (if creating a library)
	if not (len(R1_FILES) == len(R2_FILES) == len(LIBS)):
        	print(lt+"ERROR: fastq file lists don't match in length")
        	sys.exit()

	# iterate through each feature sequence and store kmers/k
	for seq in FEATURES:
		#add kmers and k to sequence
		sequence, match_threshold = seq[1], seq[2]
		kmers = kmers_k(sequence, WORDSIZE)
		seq.append(kmers)


def create_paths(run_name):

	# create results directory if it does not exist.
	if not os.path.exists("results"):
		os.makedirs("results")

	# create results/run_name/ directory, if it does not exist
	if not os.path.exists('results/'+run_name):
		os.makedirs('results/'+run_name)

def create_library(r1, r2, library_name, run_name):

	#if the library ('results/run_name/library_name') already exists, move to next library.
	if os.path.exists('results/'+run_name+"/"+library_name):
		print(library_name + ' already exists... skipping!')

	#Otherwise, make a library folder and fill it up with relevant library files
	else:
		os.makedirs('results/'+run_name+"/"+library_name)
		print(lt+'Making ' + library_name + '...')
		merge_reads(r1, r2, library_name, run_name, BIN_DIR, DATA_DIR)
		collate(library_name, run_name)
		#feature_count(FEATURES, library_name, run_name)
		feature_trim(FEATURES, library_name, run_name)
		remove_duplicates(library_name, run_name)

if __name__ == "__main__":

	# set logo type (lt) and run name variable
	lt = "[TEASEQ] "
	RUN_NAME = sys.argv[1]

	print(lt+"Checking parameters...")
    	validate_parameters()

	print(lt+"Creating required file paths...")
	create_paths(RUN_NAME)

	print("Creating libraries...")
	for lib in range(len(LIBS)): #create library from each pair of fastq files...
		create_library(R1_FILES[lib], R2_FILES[lib], LIBS[lib], RUN_NAME)