class FileManager:

    @staticmethod
    def get_filesdata(filename, emails=False):
        if emails:
            with open(filename) as f:
                lines = f.read().splitlines()
        else:
            with open(filename, encoding='utf-8') as f:
                lines = f.read().splitlines()
        return lines

    @staticmethod
    def remove_line_by_index(filename, linetoskip):
        with open(filename, 'r') as read_file:
            lines = read_file.readlines()

        currentLine = 1
        with open(filename, 'w') as write_file:
            for line in lines:
                if currentLine == linetoskip:
                    pass
                else:
                    write_file.write(line)
                currentLine += 1

    @staticmethod
    def remove_line_by_text(filename, text):
        with open(filename, 'r') as fr:
            lines = fr.readlines()

        with open(filename, 'w') as fw:
            for line in lines:
                if line.find(text) == -1:
                    fw.write(line)
