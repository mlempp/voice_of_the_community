'''
Autor: Martin Lempp

Kurzbeschreibung:
write report for results
'''
import os
import numpy as np
import codecs

def generate_report(result_dct):

    path = os.getcwd() + '/'
    with open(path+"report_template/votc_template_filled.html", "r", encoding='utf-8') as f:
        template = f.read()

    block_start, block_mid_end = template.split('<!--midblock_start-->')
    block_mid, block_end = block_mid_end.split('<!--midblock_end-->')

    final_report = block_start
    for analysis in result_dct.keys():
        tmp = result_dct[analysis]
        tmp_block = block_mid
        tmp_block = tmp_block.replace('analysisname', str(analysis))
        tmp_block = tmp_block.replace('positive_partial_deg', str(180*tmp['part_pos_coms']))
        tmp_block = tmp_block.replace('neutral_partial_deg', str(180*tmp['part_neu_coms']))
        tmp_block = tmp_block.replace('negative_partial_deg', str(180*tmp['part_neg_coms']))
        tmp_block = tmp_block.replace('positive_partial', str(int(round(tmp['part_pos_coms']*100,0))))
        tmp_block = tmp_block.replace('neutral_partial', str(int(round(tmp['part_neu_coms']*100,0))))
        tmp_block = tmp_block.replace('negative_partial', str(int(round(tmp['part_neg_coms']*100,0))))
        tmp_block = tmp_block.replace('haufigstefarbe', str(tmp['most_freq_color']))
        tmp_block = tmp_block.replace('seltenstefarbe', str(tmp['least_freq_color']))
        tmp_block = tmp_block.replace('haufigstemarke', str(tmp['most_freq_brand']))
        tmp_block = tmp_block.replace('seltenstemarke', str(tmp['least_freq_brand']))
        tmp_block = tmp_block.replace('haufigstesmodell', str(tmp['most_freq_model']))
        tmp_block = tmp_block.replace('seltenstesmodell', str(tmp['least_freq_model']))
        tmp_block = tmp_block.replace('haufigstesbauteil', str(tmp['most_freq_part']))
        tmp_block = tmp_block.replace('seltenstesbauteil', str(tmp['least_freq_part']))
        rand_nice_comment = tmp['rand_pos_comment']
        num_com_lines = np.ceil(len(rand_nice_comment) /140)
        if num_com_lines == 1:
            tmp_block = tmp_block.replace('comment_margin', str(-40))
        elif num_com_lines == 2:
            tmp_block = tmp_block.replace('comment_margin', str(-70))
        elif num_com_lines == 3:
            tmp_block = tmp_block.replace('comment_margin', str(-100))
        tmp_block = tmp_block.replace('rand_nice_comment', str(rand_nice_comment))

        final_report = final_report+tmp_block

    final_report = final_report+block_end

    return final_report

