

import yaml
import subprocess
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='ats_optimizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    """Load agent configuration from YAML file"""
    try:
        with open('agent_config.yaml') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Config load error: {str(e)}")
        raise

def run_agent(agent_name, config):
    """Execute an agent with its configured parameters"""
    agent = config['agents'][agent_name]
    cmd = [
        'python', f'{agent_name}.py',
        '--input', json.dumps(agent['input']),
        '--output', agent['output'],
        '--params', json.dumps(agent.get('parameters', {}))
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info(f"{agent_name} executed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"{agent_name} failed: {e.stderr}")
        return None

def main():
    config = load_config()
    logging.info("Starting FOD ATS optimization pipeline")
    
    for agent in config['workflow']:
        logging.info(f"Running agent: {agent}")
        result = run_agent(agent, config)
        if not result:
            logging.error(f"Pipeline halted at {agent}")
            return
        
        print(f"{agent} completed: {result[:100]}...")
    
    logging.info("Pipeline completed successfully")
    print("Resume optimization complete!")

if __name__ == "__main__":
    main()

