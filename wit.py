# Upload 177
import sys


from my_wit_project import Add, Branch, Check_out, Commit, Graph, Init, Merge, Status


if __name__ == '__main__':
    if sys.argv[1] == 'init':
        Init.init()
    elif sys.argv[1] == 'add':
        Add.add(sys.argv[2])
    elif sys.argv[1] == 'commit':
        Commit.commit()
    elif sys.argv[1] == 'status':
        Status.status()
    elif sys.argv[1] == 'checkout':
        Check_out.checkout()
    elif sys.argv[1] == 'graph':
        Graph.graph()
    elif sys.argv[1] == 'branch':
        Branch.wit_branch()
    elif sys.argv[1] == 'merge':
        Merge.merge()
# Reupload 177
