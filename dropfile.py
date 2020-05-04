import argparse
import time
import preprocessing
import numpy as np

# cosine similarity
def cosine_similarity(A,B):
  ndA = np.asarray(A)
  ndB = np.asarray(B)
  return np.dot(ndA,ndB)/(np.linalg.norm(ndA)*np.linalg.norm(ndB))


# main body of program: DropFile
# input : input file path, root path 
# output : recommended path
def dropfile(input_file: str, root_path: str):
  # preprocessing : lookup hierarchy of root path
  dir_hierarchy = preprocessing.lookup_directory(root_path)
  file_list = list()
  dir_list = list()
  label_num = 0
  for tar_dir in dir_hierarchy:
    file_list += dir_hierarchy[tar_dir]
    dir_list.append(tar_dir)
    label_num += 1
  
  # preprocessing : build list of BoW
  bow_list = list()
  for file in file_list:
    bow_list.append(preprocessing.build_BoW(file))
  
  # preprocessing : build DTM, vocab_list of files under root_path
  vocab_list, DTM = preprocessing.build_DTM(bow_list)
  
  # preprocessing : build BoW, DTM score of input file
  inbow = preprocessing.build_BoW(input_file)
  dtm_vec = preprocessing.build_DTMvec(inbow,vocab_list)
  
  # similarity calculation using cosine similarity
  sim_vec = list()
  for i in range(len(DTM)):
    sim_vec.append(cosine_similarity(DTM[i],dtm_vec))
  
  # calculate label score
  # result will be score of each directory
  label_score = [0.0 for i in range(label_num)]
  offset = 0
  for label, tar_dir in enumerate(dir_list):
    file_num = len(dir_hierarchy[tar_dir])
    for j in range(file_num):
      label_score[label] += sim_vec[offset+j]
    label_score[label] /= file_num
    offset += file_num

  # find directory that has maximum score
  dir_path = dir_list(label_score.index(max(label_score)))
  return dir_path


# main execution command
if __name__=='__main__':
  parser = argparse.ArgumentParser(description='dropFile program')
  parser.add_argument('-r', '--root-path', help='root path that input file should be classified into',
                      type=str, action='store', default='./test')
  parser.add_argument('-i', '--input-file', help='input file initial path',
                      type=str, action='store')
  args = parser.parse_args()
  
  if (args.input_file is None):
    parser.error("--input-file(-i) format should be specified")
  
  print("Running DropFile...")
  start = time.time()
  recommendation_path = dropfile(args.input_file, args.root_path)
  print("elapsed time: {}sec".format(time.time()-start))
  print("Execution Result: {}".format(recommendation_path))