from openinference.semconv.resource import ResourceAttributes
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from securebot_sdk.core.config import get_config
from securebot_sdk.logger import configure_logging

logger = configure_logging()


class Tracing:
    """Class to handle tracing setup and configuration."""

    def __init__(self, token: str):
        self.config = get_config()
        self.token = token
        self.service_name = "securebot-sdk"
        self.service_version = "1.0.0"
        self.tracer_provider = None

        try:
            logger.info(
                "Setting up tracing for session with ID: %s", self.config.project_id
            )

            # Set up resource attributes
            resource = Resource(
                attributes={
                    ResourceAttributes.PROJECT_NAME: self.config.project_id,
                    "service.name": self.service_name,
                    "service.version": self.service_version,
                    "project.id": self.config.project_id,
                    "session.id": self.config.session_id,
                }
            )
            self.tracer_provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(self.tracer_provider)

            # OTLP Exporter
            otlp_exporter = OTLPSpanExporter(
                endpoint=self.config.trace_endpoint,
                headers={
                    "Authorization": f"Bearer {self.token.access_token}",
                },
                timeout=30,
            )

            self.tracer_provider.add_span_processor(
                BatchSpanProcessor(
                    otlp_exporter,
                    max_queue_size=2048,
                    schedule_delay_millis=1000,
                    max_export_batch_size=512,
                )
            )

        except (ValueError, RuntimeError) as e:
            logger.error("Failed to setup tracing: %s", str(e))
            raise

    def get_tracer(self):
        """Get the tracer for the session."""
        return self.tracer_provider.get_tracer(__name__)

    def shutdown(self):
        """Shutdown the tracer provider and clean up resources."""
        if self.tracer_provider:
            try:
                self.tracer_provider.shutdown()
                logger.info("Tracing provider shutdown successfully")
            except RuntimeError as e:
                logger.error("Failed to shutdown tracing provider: %s", str(e))
