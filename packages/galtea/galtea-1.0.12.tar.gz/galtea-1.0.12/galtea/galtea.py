from galtea.application.services.test_case_service import TestCaseService
from .application.services.evaluation_task_service import EvaluationTaskService
from .application.services.metric_type_service import MetricTypeService
from .application.services.product_service import ProductService
from .application.services.test_service import TestService
from .application.services.version_service import VersionService
from .application.services.evaluation_service import EvaluationService
from .infrastructure.clients.http_client import Client

class Galtea:
  def __init__(self, api_key: str):
    self.__client = Client(api_key)
    self.products = ProductService(self.__client)
    self.tests = TestService(self.__client, self.products)
    self.test_cases = TestCaseService(self.__client, self.tests)
    self.versions = VersionService(self.__client, self.products)
    self.metrics = MetricTypeService(self.__client)
    self.evaluations = EvaluationService(self.__client, self.products)
    self.evaluation_tasks = EvaluationTaskService(self.__client, self.evaluations)