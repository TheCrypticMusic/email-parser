import re


class EmailParser:

    def __init__(self):
        self.email = {"To:": "", "From:": "", "Subject:": "", "Content:": ""}

    def open_file(self, file):
        if file.endswith(".eml"):
            with open(file, "r") as f:
                self.file = f.readlines()
        else:
            raise ValueError("Please import a file that ends in .EML")

    def email_to(self):
        return self.email["To:"]

    def email_from(self):
        return self.email["From:"]

    def email_subject(self):
        return self.email["Subject:"]

    def email_content(self):
        return self.email["Content:"]

    def reset_values(self):
        for headers in self.email:
            self.email[headers] = ""

    def parse_email(self):
        for headers in self.email:
            if headers != "Content:":
                self._obtain_headers(headers)
            else:
                self._obtain_content_start()
                self._obtain_content_end()
                self._obtain_content()

    def remove_tags(self):
        non_breaking_space = "&nbsp;"
        tag_removal = re.compile(r"<.*?>|\[|]||'|&quot;|=E2=80=99|&amp;|")
        content = self.email["Content:"]
        cleaned_data = re.sub(tag_removal, '', content)
        cleaned_data = cleaned_data.split("=\\n,")
        email = []
        sentence = ''
        for line in range(len(cleaned_data)):
            if non_breaking_space in cleaned_data[line]:
                if cleaned_data[line].strip().endswith(non_breaking_space) or cleaned_data[line].strip().startswith(non_breaking_space):
                    sentence += cleaned_data[line].replace(non_breaking_space, "\n").strip(" ")
                    continue
                else:
                    sentence += cleaned_data[line].replace(non_breaking_space, "\n").strip(" ")
                    email.append(sentence.strip(" "))
                    sentence = ''
            else:
                sentence += cleaned_data[line]
                email.append(sentence.strip(" "))
                sentence = ''
        return "".join(email)


    def _obtain_headers(self, header):
        for line in self.file:
            if header in line.split():
                self.email[header] = line.split(":")[-1].strip("\n").strip()
                break
            else:
                continue

    def _obtain_content_start(self):
        line_number = 0
        for line in self.file:
            if "<body" in line:
                self.start = line_number
            elif "<body>" in line:
                self.start = line_number
            line_number += 1

    def _obtain_content_end(self):
        line_number = 0
        for line in self.file:
            if "</body>" in line:
                self.end = line_number
            line_number += 1

    def _obtain_content(self):
        email_content = self.file[self.start:self.end]
        self.email["Content:"] = str(email_content)
