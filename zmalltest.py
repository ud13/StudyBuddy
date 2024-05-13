from studybuddy_utils.reasoning import SBChains

if __name__ == "__main__":
    retriever = None
    file = "./data/AI-Powered_Search_v20_Chap2.pdf"
    sbd = SBChains(retriever)
    result = sbd.find_topics(file)
    print(result)