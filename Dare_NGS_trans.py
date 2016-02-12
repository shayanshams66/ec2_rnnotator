from optparse import OptionParser
import logging
import os
class run(object):
	def __init__(self):
	self.parser()
	self.log_editor()
	logging.warning('starting Dare_NGS_Trans')
	self.run_preprocess()

	def log_editor(self):
		logging.basicConfig(filename='Dare_NGS_Trans.log',format='%(asctime)s %(message)s')
		
	def parser(self):
		parser = OptionParser()
		parser.add_option("-env", action="store",type="string", dest="environment",default="ec2",,help="Define the destination to run Rnnotator")
		parser.add_option("-i", action="store",type="string", dest="input",help="Define the destination to run Rnnotator")
		parser.add_option("-Ropt", action="store",type="string", default=None dest="rnnotator_option",help="choose single end or paired end input")
		parser.add_option("-in", action="store",type="int", default=False dest="insert_length",help="choose insert length")
		parser.add_option("-a", action="store",type="string", default="velvet" dest="assembler",help="choose assembler to run")
		parser.add_option("-n", action="store",type="int", default=1 dest="processor",help="choose number of processors")
		(options, args) = parser.parse_args()
		if len(args) != 1:
	        parser.error("wrong number of arguments")
	        self.logging.warning('wrong number of arguments')
	    environment_options={"ec2","delta","openstack"}
	    if options.environment not in environment_options:
	    	print " please choose suitable system to run Rnnotator"
	    	self.logging.warning('not suitable option for environment')
	    	sys.exit(1)
	    if options.input==None:
	    	print "define the input file"
	    		self.logging.warning('no input file defined')
	    		sys.exit(1)

	    self.env=options.environment
	    self.assembler=options.assembler
	    self.processor=options.processor
	    self.length=options.insert_length
	    self.rnnotator_opt=options.rnnotator_option
	    self.input=options.input

	def run_radical_pilot(self,input_file,script,rnn_option,kmerlength,length):
		cmd="qsub -sync y -cwd -b y -V python" + script + input_file +rnn_option+length+self.processor+kmerlength
		self.success=os.system("cmd")

    	
	def run_preprocess():
		if self.env=="ec2":
			script="radical_pilot_ec2.py"
		if self.env=="delta":
			script="radical_pilot_delta.py"
		if self.env=="openstack":
			script="radical_pilot_openstack.py"
		kmer=None
		length=self.length		
		self.run_radical_pilot(self.input,script,self.rnnotator_option,kmer,length)
		if self.success==0:
			self.logging.warning('preprocessing finished')
			kmerlength=[]
			with open("rnnotator_log.txt") as search:
    			for line in search:
        			line = line.rstrip()
        			if line.split()[0] == "kmer_length":
        				kmerlength.append(line.split()[1])
        			if line.split()[0] == "output":
        				self.assembly_input=str(line.split()[1])	
        	self.kmer_lngth=kmerlength
        	self.logging.warning('kmer lengths obtained from preprocess arekmerlength are'+kmerlength)
        	self.run_assembly()
        else:
			print ("preprocessing failed check logs")
			self.logging.warning('preprocessing failed')
			sys.exit(1)

	def run_assembly(self):
		self.logging.warning('starting multi-node assembly')
		if self.env=="ec2":
			if self.assembler=="Ray":
				script="radical_pilot_ec2_ray.py"
			if self.assembler=="contrail":
				script="radical_pilot_ec2_contrail.py"
			if self.assembler=="Abyss":
				script="radical_pilot_ec2_abyss.py"
		if self.env=="delta":
			if self.assembler=="Ray":
				script="radical_pilot_delta_ray.py"
			if self.assembler=="contrail":
				script="radical_pilot_delta_contrail.py"
			if self.assembler=="Abyss":
				script="radical_pilot_delta_abyss.py"
		if self.env=="openstack":
			if self.assembler=="Ray":
				script="radical_pilot_os_ray.py"
			if self.assembler=="contrail":
				script="radical_pilot_os_contrail.py"
			if self.assembler=="Abyss":
				script="radical_pilot_os_abyss.py"
		rnn_option=None
		length=None
		for item in self.kmer_lngth:
			message="submiting rp job for kmer"+item
			self.logging.warning('message')		
			self.run_radical_pilot(self.assembly_input,script,rnn_option,item,length)
		if self.success==0:
			self.logging.warning('assembly finished')
			with open("rnnotator_log.txt") as search:
    			for line in search:
        			line = line.rstrip()
        			if line.split()[0] == "output_assembly":
        				self.assembly_output = str(line.split()[1])	
        	self.logging.warning("assembly file output is"+)
        	self.run_postprocessing()
        else:
			print ("assemby has failed check logs")
			self.logging.warning('assembly failed')
			sys.exit(1)

	def run_postprocessing(self):
		self.logging.warning('starting post_processing')
		if self.env=="ec2":
			script="radical_pilot_ec2_pp.py"
		if self.env=="delta":
			script="radical_pilot_delta_pp.py"
		if self.env=="openstack":
				script="radical_pilot_os_pp.py"
		rnn_option=None
		length=None
		kmer=None
		self.run_radical_pilot(self.assembly_output,script,rnn_option,kmer,length)
		if self.success==0:
			self.logging.warning('Rnnotator is finished check the directory for output')
        else:
			print ("postprocessing has failed")
			self.logging.warning('postprocessing has failed')
			sys.exit(1)

			
def main():
	runner=run()		
if __name__ == "__main__":
    main()			



				





