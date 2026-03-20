from processor.processor_regex import classify_with_regex
from processor.processor_bert import classify_with_bert
from processor.processor_llm import classify_with_llm
import pandas as pd

def classify(logs):
    labels = []
    for source, log in logs:
        label = classify_log(source, log)
        labels.append(label)
    return labels


def classify_log(source, log_message):
    # Strip the log_message
    clean_message = log_message.strip()

    if source == "LegacyCRM":
        label = classify_with_llm(clean_message)
    else:
        label = classify_with_regex(clean_message)
        if not label:
            label = classify_with_bert(clean_message)

    return label


def classify_csv(input_file):
    df = pd.read_csv(input_file)
    #perform classification
    df['label'] = classify(list(zip(df['source'], df['log_message'])))

    #create an Output file
    output_file = "resources/output.csv"
    df.to_csv(output_file, index=False)

    return output_file


if __name__ == '__main__':
    classify_csv('resources/test.csv')

    """
     logs = [
         ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
         ("BillingSystem", "User User12345 logged in."),
         ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
         ("AnalyticsEngine", "Backup completed successfully."),
         ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
         ("ModernHR", "Admin access escalation detected for user 9429"),
         ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
         ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
         ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
         ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"),
         ("ModernHR", "Hey Bro, chill ya!")
     ]

     classified_logs = classify(logs)

     for log, label in zip(logs, classified_logs):
         print(log[1], "->", label)
    """
