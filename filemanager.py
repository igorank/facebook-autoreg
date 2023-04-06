class FileManager:

    @staticmethod
    def get_filesdata(filename, emails=False):
        if emails:
            with open(filename) as file:
                lines = file.read().splitlines()
        else:
            with open(filename, encoding='utf-8') as file:
                lines = file.read().splitlines()
        return lines

    @staticmethod
    def remove_line_by_index(filename, linetoskip):
        with open(filename, 'r') as read_file:
            lines = read_file.readlines()

        current_line = 1
        with open(filename, 'w') as write_file:
            for line in lines:
                if current_line == linetoskip:
                    pass
                else:
                    write_file.write(line)
                current_line += 1

    @staticmethod
    def remove_line_by_text(filename, text):
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file_w:
            for line in lines:
                if line.find(text) == -1:
                    file_w.write(line)
