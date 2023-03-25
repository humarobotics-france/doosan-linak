import time

linak = Linak(ip="192.168.1.10", port=502)

th_id = thread_run(linak.heartbeat, loop = True)
tp_log(str(linak.get_position()))
time.sleep(5)
linak.move_to(0, 100)
time.sleep(5)
tp_log(str(linak.get_position()))
linak.move_to(100, 100)
time.sleep(2)

thread_stop(th_id)
linak.close_connexion()
