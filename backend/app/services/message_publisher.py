import pika
import json
from app.config import settings


class MessagePublisher:
    
    def __init__(self):
        self.queue_name = "message_processing_queue"
    
    def publish_message(self, message_id: int, content: str):

        try:

            connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            channel = connection.channel()
            

            channel.queue_declare(
                queue=self.queue_name,
                durable=True
            )
            
            message_data = {
                "message_id": message_id,
                "content": content
            }
            
            channel.basic_publish(
                exchange='',
                routing_key='message_processing_queue',
                body=json.dumps(message_data),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            print(f"Mensagem publicada: ID={message_id}")
            
            connection.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao publicar: {e}")
            return False



message_publisher = MessagePublisher()