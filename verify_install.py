import sys
import pkg_resources
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

required_packages = {
    'fastapi': 'fastapi[all]',
    'python-dotenv': 'python-dotenv',
    'crewai': 'crewai',
    'langchain': 'langchain',
    'langchain-core': 'langchain-core',
    'transformers': 'transformers',
    'torch': 'torch',
    'uvicorn': 'uvicorn[standard]',
    'httpx': 'httpx',
    'python-multipart': 'python-multipart'
}

def verify_imports():
    missing_packages = []
    
    for package, install_name in required_packages.items():
        try:
            pkg_resources.get_distribution(package)
            logger.info(f"✓ {package} installed successfully")
        except pkg_resources.DistributionNotFound:
            logger.error(f"✗ {package} not found")
            missing_packages.append(install_name)
    
    if missing_packages:
        logger.error("\nMissing packages. Install them with:")
        logger.error(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    else:
        logger.info("\nAll required packages are installed!")

if __name__ == "__main__":
    verify_imports() 