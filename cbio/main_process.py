import os
import subprocess
from .utils import utils

class BioTask():
    def __init__(self, config):
        self.config = config

        self.log = utils.set_log(__name__, config['log_files'])

    def build_global_params(self):
        # Options
        self.sampleID = self.config['sampleID']
        self.build = self.config['process_conf']['build']

        script_path = os.path.dirname(os.path.realpath(__file__))

        # Software
        self.BWAPATH = self.config['softdata']['software']['paths']['BWAPATH']
        self.SAMTOOLSPATH = self.config['softdata']['software']['paths']['SAMTOOLSPATH']
        self.FREEBAYESPATH = self.config['softdata']['software']['paths']['FREEBAYESPATH']
        self.ANNOVARPATH = self.config['softdata']['software']['paths']['ANNOVARPATH']
        self.BEDTOOLSPATH = self.config['softdata']['software']['paths']['BEDTOOLSPATH']
        self.PICARDPATH = self.config['softdata']['software']['paths']['PICARDPATH']
        self.SNPEFFPATH = self.config['softdata']['software']['paths']['SNPEFFPATH']
        self.SNPSIFTPATH = self.config['softdata']['software']['paths']['SNPSIFTPATH']
        self.FASTQCPATH = self.config['softdata']['software']['paths']['FASTQCPATH']
        self.BGZIPPATH = self.config['softdata']['software']['paths']['BGZIPPATH']
        self.TABIXPATH = self.config['softdata']['software']['paths']['TABIXPATH']
        self.ABRA = self.config['softdata']['software']['paths']['ABRA']
        self.BBDUKPATH = self.config['softdata']['software']['paths']['BBDUKPATH']
        self.KARTPATH = self.config['softdata']['software']['paths']['KARTPATH']
        self.RTGPATH = self.config['softdata']['software']['paths']['RTGPATH']
        self.VCFALLELICPRIM = self.config['softdata']['software']['paths']['VCFALLELICPRIM']
        self.VT = self.config['softdata']['software']['paths']['VT']
        self.SORTBED = self.config['softdata']['software']['paths']['SORTBED']
        self.GEMINIPATH = self.config['softdata']['software']['paths']['GEMINIPATH']
        self.VEPPATH = self.config['softdata']['software']['paths']['VEPPATH']

        # Other
        self.REFERENCE_GENOME = self.config['softdata']['ref'][self.build]
        self.HUMANDB = self.config['softdata']['dbs']['ANNOVARINFO']
        self.NEXTERAPE = os.path.join("/DATA/biodata/NexteraPE-PE.fa")
        self.VEPCACHE = self.config['softdata']['software']['paths']['VEPCACHE']
        self.VEPDB = self.config['softdata']['dbs']['VEPDB']


        return None

    def configure_tool(self, config):
        self.config = config
        self.log = utils.set_log(__name__, config['log_files'])

        self.build_global_params()

    def make_tests(self):
        self.check_config()
        self.check_reference_genome()

    def run(self):
        import time
        start = time.time()
        # self.loggerApi.iniciar_paso(type(self).__name__, self.config['process_conf']['sample']['modality'], self.log)

        # Ejecutar la herramienta
        self.run_process()

        # Finalizacion
        end = time.time()
        time = str(round(end - start, 2))
        self.log.debug(f'_time_ - {type(self).__name__} - {time} s')
        # self.loggerApi.finalizar_paso(type(self).__name__, self.config['process_conf']['sample']['modality'], self.log)
        # self.loggerApi.informar(f"{type(self).__name__} result")

    def check_config(self):
        pass

        # try:
        #     assert set(self.config.keys()) == set(['DEBUG', 'TESTING', 'DRY_RUN', 'sampleID',
        #                                         'outfolder', 'url', 'log_files',
        #                                         'process_conf', 'tools_conf', 'softdata'])
        #     assert list(self.tool_config.keys()) == ['input', 'output', 'software', 'tool_conf']
        #     return True
        # except:
        #     self.log.error(type(self).__name__)
        #     self.log.error("Assert error while checking configuration")
        #     self.log.error(self.config.keys())
        #     self.log.error(str(['DEBUG', 'TESTING', 'DRY_RUN', 'sampleID',
        #                                         'outfolder', 'url', 'log_files',
        #                                         'process_conf', 'tools_conf', 'softdata']))
        #     self.log.error(self.tool_config.keys())
        #     self.log.error(str(['input', 'output', 'software', 'tool_conf']))
        #     raise Exception("Configuration doesn't match")
        #     return False

    def check_reference_genome(self):
        """
        Function that checks the reference genome used by the user. By the time,
        just a list of reference genomes could be used to do the mapping of
        sequences.

        Parameters
        ----------
        user_ref : str
            String with the reference genome that is going to be used

        Returns
        -------
        user_ref : str
            Same string validated
        """
        if self.build in ['GRCh37', "GRCh38", "hg19", "hg38", "hs37d5"]:
            return self.build
        else:
            raise Exception("Version \"" + self.build + "\" still not available")

    def cmd_run(self, mode=1):
        import time
        cmd = self.build_cmd()

        # If dry_run, don't run the process, just print it
        if self.config['DRY_RUN'] is True:
            self.log.info('Generating CLI command...')
            self.log.info(cmd)

        else:
            if mode == 1:
                self.log.info('Running command...')
                process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out = None
                err = None

                self.log.debug("Printing software log:")
                while out != "" or err != "":
                    out = process.stdout.readline()
                    err = process.stderr.readline()
                    out = out.decode("utf-8").strip('\n')
                    err = err.decode("utf-8").strip('\n')
                    self.log.debug(err)
                    self.log.debug(out)

            elif mode == 2:
                os.system(cmd)

            elif mode == 3:
                f = open("/tmp/full.bwa.log", "w+")
                # Using pipe in command could block the stdout, see this post:
                # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
                # https://www.reddit.com/r/Python/comments/1vbie0/subprocesspipe_will_hang_indefinitely_if_stdout/
                self.log.info('Running command...')
                process = subprocess.Popen(cmd, shell=True, executable='/bin/bash',
                                 stdout=f, stderr=f)
                while process.poll() is None:
                    time.sleep(5)

                f.close()

        self.log.info(f"Finished process {type(self).__name__}")

    def get_task_options(self):
        return(self.tool_config)
