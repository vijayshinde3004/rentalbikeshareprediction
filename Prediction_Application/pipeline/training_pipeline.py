
from Prediction_Application.components.model_trainer import ModelTrainer
from Prediction_Application.logger import logging
from Prediction_Application.exception import ApplicationException
from Prediction_Application.components.data_ingestion import DataIngestion
from Prediction_Application.components.data_validation import DataValidation
from Prediction_Application.components.data_transformation import DataTransformation
from Prediction_Application.config.configuration import Configuration
from Prediction_Application.entity.config_entity import DataIngestionConfig
from Prediction_Application.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact, ModelTrainerArtifact
import os,sys

# Wee need data so that we can perfrom our complete operations -> Data -> Data Ingestion / Data Extraction
# Data Validation
# a-> INT, b -> INT: 

class Training_Pipeline:

    def __init__(self,config: Configuration=Configuration())->None:
        try:
            logging.info(f"\n{'*'*20} Initiating the Training Pipeline {'*'*20}\n\n")
            self.config = config
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def start_data_ingestion(self,data_ingestion_config:DataIngestionConfig)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def start_data_validation(self, data_ingestion_config:DataIngestionConfig,
                                    data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_config = data_ingestion_config,
                                             data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise ApplicationException from e

# We are handling outliers, Handling Imblanced Data, Handling Missing values, Data Distribution, Checking Duplicated,
# Do the Encdoing, Scaling, 
# -> We need data -> Data Ingestion Artifact -> We need to validate to perfrom data transfromation operation
   
    def start_data_transformation(self,data_ingestion_artifact: DataIngestionArtifact,
                                       data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config = self.config.get_data_transformation_config(),
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_artifact = data_validation_artifact)

            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise ApplicationException(e,sys) from e


    def start_model_training(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                        data_transformation_artifact=data_transformation_artifact)   

            return model_trainer.initiate_model_training()
        except Exception as e:
            raise ApplicationException(e,sys) from e               

    def run_training_pipeline(self):
        try:
            data_ingestion_config=self.config.get_data_ingestion_config()

            data_ingestion_artifact = self.start_data_ingestion(data_ingestion_config)

            data_validation_artifact = self.start_data_validation(data_ingestion_config=data_ingestion_config,
                                                            data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                             data_validation_artifact=data_validation_artifact)

            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)         
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def __del__(self):
        logging.info(f"\n{'*'*20} Training Pipeline Complete {'*'*20}\n\n")