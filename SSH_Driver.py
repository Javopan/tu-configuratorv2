import paramiko
import time


class SikluSsh:
    """
    This class will use the default parameters of the radio from siklu
    """
    def __init__(self, ip='192.168.0.1', username='admin', password='admin', port=22, timeout=10, wait_for_buffer=0.1,
                 addpolicy=True):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.wait_for_buffer = wait_for_buffer
        self.ssh = None
        self.addpolicy = addpolicy
        self.channel = None

    def connect(self):
        """
        Creates a connection with the given parameters via a SSH Shell.
        By default it will auto add keys
        :return:
        """
        self.ssh = paramiko.SSHClient()
        if self.addpolicy:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.ip, port=self.port, username=self.username, password=self.password)
            self.channel = self.ssh.invoke_shell()
            return True
        except:
            return False

    def send_command(self, command_):
        """
        This fuction will send the commands to the radio via SSH shell.
        We will get the result in the in the same channel in the in_buffer as bytes
        We also have to wait until the in_buffer gets some information or until the
        timeout happens and break the connection
        :param command_:
        Command will be the command to execute.
        :return:
        """
        self.channel.send(command_ + '\n')
        start = time.time()
        while len(self.channel.in_buffer) == 0 and time.time() < start + self.timeout:
            # wait until time out or buffer size is bigger than 0
            time.sleep(self.wait_for_buffer)
        buffer_size = len(self.channel.in_buffer)
        if buffer_size > 0:  # If the buffer has something
            buffer_size = len(self.channel.in_buffer)
            time.sleep(self.wait_for_buffer)
            while len(self.channel.in_buffer) > buffer_size:  # we will check that the buffer will be static
                buffer_size = len(self.channel.in_buffer)
                time.sleep(self.wait_for_buffer)
            # buffer = self.channel.in_buffer._buffer
            return self.channel.in_buffer.read(len(self.channel.in_buffer))
        return None

    def close(self):
        self.ssh.close()


class Answer:
    """
    This class will process the answers of the radios to poll
    """
    def __init__(self, text, command, cli_marker='>', before_name='\r\n\r\n'):
        self.text = text
        self.cli_marker = cli_marker
        self.before_name = before_name
        self.command = command

    def process_text(self):
        if self.text:
            self.text = self.text.decode()
            self.text = self.text.strip()
            self.text = self.text.replace(self.command, '')
            if self.text.find(self.cli_marker) < len(self.text) // 2:  # the starting marker is on the start of the line
                self.text = self.text.strip()
                self.text = self.text[self.text.find(self.cli_marker) + 1:]  # remove the cli marker of the equipment
            if self.text.find(self.cli_marker) > len(self.text) // 2:  # the line end is at the end of the line
                self.text = self.text[:self.text.rfind('\r\n')]
            return [element for element in self.text.split('\r\n') if len(element) > 0]
        return []


if __name__ == '__main__':
    ip_to_read = '192.168.1.50'
    command = 'copy startup-configuration display'

    ssh = SikluSsh(ip_to_read, 'admin', 'admin')
    try:
        ssh.connect()
    except paramiko.AuthenticationException:
        print("Couldn't log to the radio")
    ssh_answer = ssh.send_command(command)
    a = Answer(ssh_answer, command)
    print(a.process_text())
    # radio_answers[ip].update({loop_n: Answer(ssh.send_command(command), command).process_text()})
    ssh.close()
