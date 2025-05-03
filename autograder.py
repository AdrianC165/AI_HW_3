import json
import re
import os
import math

test_cases = [
    # name, fn, display, max_score
    ('Demo', 'demo.out', True, 0),
    ('task6', 'task6.out', True, 0),
    ('task7', 'task7.out', True, 0),
    ('task1.in', 'task1.in', False, 5),
    ('task2.in', 'task2.in', False, 5),
    ('task3.in', 'task3.in', False, 5),
    ('Hidden test case 1', 'clause1.out', False, 20),
    ('Hidden test case 2', 'clause2.out', False, 20),
    ('Hidden test case 3', 'clause3.out', False, 20),
    ('Hidden test case 4', 'clause4.out', False, 20),
]

def lower_set(s):
    return set([_.lower() for _ in s])

def deal(stu_line, gold_line):
    # print(gold_line)
    stu_line = stu_line.strip()
    gold_line = gold_line.strip()
    # print(gold_line)
    format_flag = True
    if stu_line.count(" ") != gold_line.count(" "):
        format_flag = False
    stu_st, stu_ed = 0, 0
    gold_st, gold_ed = 0, 0
    if '{' not in gold_line:
        stu_st = len(stu_line)
        gold_st = len(gold_line)
        stu_ed = stu_st
        gold_ed = gold_st
    for i in range(len(stu_line)):
        if stu_line[i] == '{':
            stu_st = i
        elif stu_line[i] == '}':
            stu_ed = i
    for i in range(len(gold_line)):
        if gold_line[i] == '{':
            gold_st = i
        elif gold_line[i] == '}':
            gold_ed = i
    lhs_stu = set([_.strip() for _ in stu_line[0:stu_st].split()])
    lhs_gold = set([_.strip() for _ in gold_line[0:gold_st].split()])
    rhs_stu = set([_.strip() for _ in stu_line[stu_st+1:stu_ed].split()])
    rhs_gold = set([_.strip() for _ in gold_line[gold_st+1:gold_ed].split()])
    content_flag = True
    if lhs_stu != lhs_gold or rhs_stu != rhs_gold:
        if lower_set(lhs_stu) != lower_set(lhs_gold) or (lower_set(rhs_stu) != lower_set(rhs_gold) and (len(rhs_stu) == 1 and len(rhs_gold) == 0 and ' ' in rhs_stu)):
            content_flag = False
        else:
            content_flag = True
            format_flag = False

    # print(stu_line)
    # print(set(re.sub('\s+', '', stu_line).split(',')))
    # print(set(re.sub('\s+', '', gold_line).split(',')))
    # print('------------')
    return (content_flag, format_flag)


def main():
    total_points = 0
    format_points = 5
    response = {}
    response['score'] = 0
    response['max_score'] = 100
    response['tests'] = []

    for test_case in test_cases:
        name, fn, display, points = test_case
        if not os.path.exists(fn):
            json_output = {}
            json_output['name'] = name
            # json_output['score'] = math.ceil(T/N * points)
            json_output['score'] = 0
            json_output['max_score'] = points
            json_output['tags'] = []
            output_str = ''
            json_output['output'] = f'{fn} does not exist.' if 'in' in fn else 'Output file does not exist.'
            response['tests'].append(json_output)
            continue

        stu_output = open(fn, 'r')
        gold_output = open(fn.split('.')[0] + '.gold.out', 'r')
        raw_stu_lines = '\n'.join(stu_output.readlines())
        raw_gold_lines = '\n'.join(gold_output.readlines())
        stu_lines = re.sub('\n+', '\n', raw_stu_lines).split('\n')
        gold_lines = re.sub('\n+', '\n', raw_gold_lines).split('\n')
        if len(stu_lines) and stu_lines[-1] == '':
            stu_lines = stu_lines[:-1]
        if gold_lines[-1] == '':
            gold_lines = gold_lines[:-1]

        N = len(gold_lines)
        T = 0

        for idx, line in enumerate(gold_lines):

            if idx >= len(stu_lines):
                break
            r_correct, f_correct = deal(stu_lines[idx], line)
            if r_correct:
                T += 1
                if not f_correct:
                    format_points = 0
            else:
                break
            # if stu_lines[idx] == line:
            #     T += 1
            # elif ''.join(stu_lines[idx].split()) == ''.join(line.split()):
            #     T += 1
            #     format_points = 0
            # elif ''.join(stu_lines[idx].split()) == ''.join(line.split('.')[1].strip().split()):
            #     T += 1
            #     format_points = 0
            # else:
            #     r_correct, f_correct = deal(stu_lines[idx], line)
            #     if r_correct:
            #         T += 1
            #         if not f_correct:
            #             format_points = 0
            #     else:
            #         break

        json_output = {}
        json_output['name'] = name
        # json_output['score'] = math.ceil(T/N * points)
        json_output['score'] = points if T == N else 0
        json_output['max_score'] = points
        json_output['tags'] = []
        output_str = ''
        if T == N:
            output_str = 'The content of your output is correct.\n\n'
            if display:
                output_str += 'The correct output for this test case is: \n'
                output_str += raw_gold_lines + '\n ========================================== \n'
                output_str += 'While your output for this test case is: \n'
                output_str += raw_stu_lines + '\n ========================================== \n'
        else:
            output_str = f'There are {N} line(s) in the correct output, while your program outputs {T} correct line(s).\n\n'
            if display:
                output_str += 'The correct output for this test case is: \n'
                output_str += raw_gold_lines + '\n ========================================== \n'
                output_str += 'While your output for this test case is: \n'
                output_str += raw_stu_lines + '\n ========================================== \n'

        json_output['output'] = output_str
        response['tests'].append(json_output)
        response['score'] += json_output['score']


    if response['score'] > 0:
        response['score'] += format_points
        if format_points == 0:
            format_str = 'The format of your output is not correct. Did you have extra/less spaces or line breaks? or did you forget the index of each line? \n'
        else:
            format_str = 'The format of your output is correct.\n'
    else:
        format_points = 0
        format_str = ''
    response['tests'].append({'name': 'Format', 'max_score': 5, 'score': format_points, 'output': format_str})
    with open('/autograder/results/results.json', 'w') as f:
        f.write(json.dumps(response))

if __name__ == '__main__':
    main()