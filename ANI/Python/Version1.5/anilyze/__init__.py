#!/user/bin/python
import ftplib#library used to download files using ftp
import os#library used to execute system commands
import time#library used to calculate total run time
from collections import OrderedDict
import sys#library used to execute system commands
import subprocess
import fileinput#library used to get file input
import shutil#library used to use shell
import Bio#library used to use seq to reverse concatinate the fna files
from Bio.Seq import Seq#library used to reverse concatinate the fna files
import getopt