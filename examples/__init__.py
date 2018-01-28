import time

from BlastApi import BlastClient

bc = BlastClient()


def example1():
    rid, rtoe = bc.search("u00001", "nt", "blastn")
    print('Request id: ' + rid)
    print(bc.check_submission_status(rid))
    time.sleep(int(rtoe))
    status = 'WAITING'
    while status == 'WAITING':
        time.sleep(2)
        status = bc.check_submission_status(rid)
    print(bc.check_submission_status(rid))
    print('#########################  HTML  #########################')
    print(bc.get_results(rid, format_type='HTML'))
    print('\n\n\n')
    print('#########################  Text  #########################')
    print(bc.get_results(rid, format_type='Text'))
    print('\n\n\n')
    print('#########################  XML  #########################')
    print(bc.get_results(rid, format_type='XML'))
    print('\n\n\n')
    print(bc.get_results(rid, format_type='XML2', results_file_path='ex1_xml2.zip'))
    print(bc.get_results(rid, format_type='JSON2', results_file_path='ex1_json2.zip'))
    print('#########################  XML  #########################')
    print(bc.get_results(rid, format_type='Tabular'))
    print('\n\n\n')


def example2():
    rid, rtoe = bc.search("u00001", "nt", "blastn")
    print('Request id: ' + rid)
    print('Estimated time: ' + rtoe)
    print(bc.wait_for_results(rid, format_type='XML2', estimated_time=rtoe))


example1()
example2()
