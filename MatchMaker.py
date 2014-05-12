"""
Author: Kevin Owens
Date: 7 May 2014
Class: MatchMaker

Problem description summary (from TopCoder Tournament Inv 2001 Semi A+B 250):  In the context of a dating application, this matches a person with
candidates who meet their gender preference and compatibility, as determined by the number of matching answers to
a set of questions.  Inputs to the required getBestMatches() are a list of strings representing the candidate pool,
each string containing the person's name, gender, gender preference, and answers to 10 questions; the name of the
person being matched; and the number of matching question answers they require.  Output is a list of names of those
persons matching the requesting member's criteria, sorted in priority order from greatest to least similarity.  Note
the order of the list is very specific; i.e., two members with the same similarity score must be returned in the same
order they were given.  This is not necessarily the result of a pure descending-order sort.
"""


class MatchMaker:

    def getBestMatches(self, member_pool: list, member_name: str, sim_factor: int) -> tuple:
        # member_pool: list of 1-50 strings of format "NAME G D X X X X X X X X X X"
        #   where NAME is case-sensitive member's name, len 1-20
        #   where G is gender, M or F
        #   where D is requested gender, M or F
        #   where Xs are member's question answers, A-D, len 1-10
        # member_name: name of requesting member
        # sim_factor: integer 1-10 representing similarity factor (e.g., 2 = 2 matching answers)
        # returns: tuple(string) list of members with sim_factor or more matching answers (not including currentUser)
        #   descending ordered by num matches

        # get current user info
        for m in member_pool:
            m_info = m.split()
            if m_info[0] == member_name:
                cu_info = m_info
        
        # for each member_name
        matches = []
        for m in member_pool:

            # break out info on member in pool
            m_info = m.split()

            # skip requesting member
            if m_info[0] == cu_info[0]:
                continue
            
            # skip undesired genders
            if m_info[1] != cu_info[2] or cu_info[1] != m_info[2]:
                continue

            # skip those with too few matching answers
            num_matches = len([i for i in range(3, len(m_info)) if m_info[i] == cu_info[i]])
            if num_matches < sim_factor:
                continue

            # add match count and member_name name to array
            matches.append((num_matches * -1, m_info[0]))
                # -1 forces correct sort order
                # e.g., matches of [(3, 'BETTY'), (4, 'ELLEN'), (3, 'MARGE')]
                # is rev sorted to [(4, 'ELLEN'), (3, 'MARGE'), (3, 'BETTY')],
                # which is wrong b/c BETTY comes before MARGE in input list.
                # Negating returns [(-4,'ELLEN'), (-3,'BETTY'), (-3,'MARGE')],
                # which places them in the correct order.
                        
        # prioritize matches in decreasing order, leaving like sim_factors in the original order
        matches.sort()

        # return just member names
        return [m[1] for m in matches]
    

if __name__ == '__main__':
    
    mm = MatchMaker()
    members = ["BETTY F M A A C C",
               "TOM M F A D C A",
               "SUE F M D D D D",
               "ELLEN F M A A C A",
               "JOE M F A A C A",
               "ED M F A D D A",
               "SALLY F M C D A B",
               "MARGE F M A A C C"]

    print('BETTY matches with', mm.getBestMatches(members, "BETTY", 2))  # ['JOE', 'TOM']
    print('JOE matches with', mm.getBestMatches(members, "JOE", 1))  # ['ELLEN', 'BETTY', 'MARGE']