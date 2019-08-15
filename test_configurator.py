from package import machine
import sys,time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_configurator(argv):
  if (len(sys.argv) < 3):
    print (sys.argv[0] + ' [machine <datafile/Data_QA.xlsx>')
    sys.exit()
  start = time.time()
  machine.validate_machine(sys.argv[1], sys.argv[2])
  elapsed_time = time.time() - start
  logging.info('Time taken to run in secs ' + str(round(elapsed_time,2)))
  
if __name__ == "__main__":
  test_configurator(sys.argv[1:])
