import redis
import threading
from loguru import logger
import traceback
from time import sleep
from typing import Union
import queue


class redis_channel:
    RAYIN_ORDER_CHANNEL_TEST = 'RAYIN_ORDER_CHANNEL_TEST'
    RAYIN_ORDER_CHANNEL_FORMAL = 'RAYIN_ORDER_CHANNEL_FORMAL'



class base_tredis_msg_sender:
    def __init__(self, tredis=None):
        self.tredis: Tredis = tredis

    def redis_msg_sender(self, channel, data):
        logger.info(f'This is what I got: {data} from {channel}')
        if self.tredis is not None and self.tredis.r is not None:
            ret = self.tredis.r.get(str(data))
            if ret is not None:
                logger.info(f'This is what I have found {ret} {type(ret)}')
                return ret
            else:
                logger.info(f'Cannot find {data} on server')
        return None


# TODO: 怪怪的，效率很差...
class Tredis_publish(threading.Thread):
    str_exit_magic_words = 'Exit Exit Exit now'

    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password=''):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.db = db
        self.password = password
        self.queue_publish = queue.Queue()
        
        # Add a pipeline for batch processing
        self.r = redis.StrictRedis(host=self.server,
                                 port=self.port,
                                 db=self.db,
                                 charset="utf-8",
                                 decode_responses=True,
                                 password=self.password)
        self.start()

    def run(self):
        while True:
            try:
                # Process messages in smaller batches
                messages_to_process = []
                # Try to get as many messages as possible without blocking too long
                for _ in range(100):  # Process up to 100 messages at once
                    try:
                        channel, message = self.queue_publish.get(timeout=0.01)  # Reduced timeout
                        messages_to_process.append((channel, message))
                        
                        if channel == self.str_exit_magic_words and message == self.str_exit_magic_words:
                            break
                    except queue.Empty:
                        break

                if messages_to_process:
                    # Use pipeline for batch processing
                    with self.r.pipeline() as pipe:
                        for channel, message in messages_to_process:
                            pipe.publish(channel, message)
                        pipe.execute()
                    
                    # Mark all processed messages as done
                    for _ in messages_to_process:
                        self.queue_publish.task_done()

                    if (self.str_exit_magic_words, self.str_exit_magic_words) in messages_to_process:
                        break
                        
            except Exception as e:
                logger.exception(f"Error in Tredis_publish: {e}")
                sleep(0.1)  # Brief pause on error before retrying

    def publish(self, channel, message):
        self.queue_publish.put((channel, message), block=True)

    def stop(self):
        self.publish(self.str_exit_magic_words, self.str_exit_magic_words)


class Tredis_subscribe(threading.Thread):
    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password='',
                 channel='test',
                 prefix='test',
                 redis_msg_sender=base_tredis_msg_sender()):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.db = db
        self.password = password
        self.channel = channel
        self.prefix = prefix
        self.redis_msg_sender = redis_msg_sender
        self.str_thread_exit_magic = 'redis thread exit'
        
        # Add a message processing queue
        self.message_queue = queue.Queue(maxsize=10000)
        
        # Connect to Redis with optimized parameters
        self.r = redis.StrictRedis(
            host=self.server,
            port=self.port,
            db=self.db,
            charset="utf-8",
            decode_responses=True,
            password=self.password,
            socket_keepalive=True,
            socket_timeout=1,
            health_check_interval=30
        )

        logger.info(f'Redis connected to {self.server}, port {self.port}, db: {self.db}')
        self.sub = self.r.pubsub(ignore_subscribe_messages=True)  # Ignore subscribe/unsubscribe messages
        logger.info(f'Redis subscribe to channel [{self.channel}]')
        
        # Subscribe to initial channel before starting thread
        self.sub.subscribe(self.channel)
        self._stop_event = threading.Event()  # Add stop event
        self.start()

    def run(self):
        while not self._stop_event.is_set():
            try:
                # Get messages in batch with a smaller timeout
                messages = self.sub.get_message(timeout=0.01)
                if messages:
                    try:
                        channel = messages['channel']
                        data = messages['data']

                        if isinstance(data, str) and data.startswith(self.str_thread_exit_magic):
                            if data[len(self.str_thread_exit_magic) + 1:] == str(self):
                                logger.info(f'{self} to exit')
                                break

                        # Process message asynchronously
                        function_send = getattr(self.redis_msg_sender, 'redis_msg_sender', None)
                        if function_send is not None and callable(function_send):
                            function_send(channel, data)
                            
                    except Exception as e:
                        if not self._stop_event.is_set():  # Only log if not stopping
                            logger.exception(f'Error processing message: {e}')

            except Exception as e:
                if not self._stop_event.is_set():  # Only log if not stopping
                    logger.exception(f'Redis subscribe error: {e}')
                sleep(0.1)  # Brief pause on error before retrying

        # Cleanup after loop ends
        try:
            if self.sub:
                self.sub.unsubscribe()
                self.sub.close()
            if self.r:
                self.r.close()
        except Exception as e:
            logger.exception(f'Error during cleanup: {e}')

    def subscribe(self, channel):
        """Subscribe to a new channel using pipeline for efficiency"""
        if not self._stop_event.is_set():
            logger.info(f'Redis subscribe to extra channel [{channel}]')
            self.sub.subscribe(channel)

    @logger.catch()
    def stop(self):
        """Stop the subscription thread safely"""
        self._stop_event.set()  # Signal the thread to stop
        try:
            if self.r and self.channel:
                self.r.publish(self.channel, f'{self.str_thread_exit_magic} {str(self)}')
        except Exception as e:
            logger.exception(f'Error during stop: {e}')


class Tredis:
    default_port = 6379
    default_db = 0

    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password='',
                 channel='test',
                 prefix='test',
                 redis_msg_sender=base_tredis_msg_sender()):
        self.tredis_subscribe = Tredis_subscribe(server, port, db, password, channel, prefix, redis_msg_sender)
        self.tredis_publish = Tredis_publish(server, port, db, password)

        self.r = self.tredis_publish.r

    def subscribe(self, channel):
        self.tredis_subscribe.subscribe(channel)

    def publish(self, channel, message):
        self.tredis_publish.publish(channel, message)

    def stop(self):
        self.tredis_subscribe.stop()
        self.tredis_publish.stop()

    def join(self):
        self.tredis_subscribe.join()
        self.tredis_publish.join()


if __name__ == '__main__':

    class warrant_channel:
        ALL = 'WARRANT_ALL'
        DEALER = 'WARRANT_DEALER'
        LARGE_VOLUME = 'WARRANT_LARGE_VOLUME'
        BURST = 'WARRANT_BURST'

        AMOUNT_STOCK_AND_WARRANT = 'AMOUNT_STOCK_AND_WARRANT'
        AMOUNT_WARRANT = 'AMOUNT_WARRANT'
        AMOUNT_STOCK = 'AMOUNT_STOCK'


    # logger.disable('mypylib.tredis')

    sender = base_tredis_msg_sender()

    tredis = Tredis(server='livewithjoyday.com',
                    port=Tredis.default_port,
                    db=Tredis.default_db,
                    password='5k4g4redisau4a83',
                    channel='warrant_command',
                    prefix='warrant',
                    redis_msg_sender=sender
                    )
    tredis_shioaji = Tredis(server='localhost',
                            port=Tredis.default_port,
                            db=Tredis.default_db,
                            password='',
                            channel='shioaji_wrapper',
                            prefix='shioaji',
                            redis_msg_sender=sender
                            )

    tredis.subscribe(warrant_channel.ALL)
    tredis.subscribe(warrant_channel.DEALER)
    tredis.subscribe(warrant_channel.LARGE_VOLUME)
    tredis.subscribe(warrant_channel.BURST)

    tredis.publish(warrant_channel.ALL, warrant_channel.ALL)
    tredis_shioaji.publish(warrant_channel.ALL, warrant_channel.ALL + ' tredis_shioaji')
    tredis.publish(warrant_channel.DEALER, warrant_channel.DEALER)
    tredis_shioaji.publish(warrant_channel.DEALER, warrant_channel.DEALER + ' tredis_shioaji')
    tredis.publish(warrant_channel.LARGE_VOLUME, warrant_channel.LARGE_VOLUME)
    tredis_shioaji.publish(warrant_channel.LARGE_VOLUME, warrant_channel.LARGE_VOLUME + ' tredis_shioaji')
    tredis.publish(warrant_channel.BURST, warrant_channel.BURST)
    tredis_shioaji.publish(warrant_channel.BURST, warrant_channel.BURST + ' tredis_shioaji')

    index = 0
    while True:
        try:
            sleep(1)
            index += 1
            if index == 3:
                break
        except KeyboardInterrupt:
            break

    tredis_shioaji.stop()
    tredis.stop()
