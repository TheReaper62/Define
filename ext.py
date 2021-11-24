import discord, json, asyncio

def MissingArgsEmbed(args):
    embed = discord.Embed(
        title = "Missing Arguments",
        description = ",".join([f"`{i}`" for i in args]) + " has not been detected or is invalid",
        colour = discord.Colour.red()
    )
    return embed

def match(given,actual):
    actual,given = given.lower(),actual.lower()
    score = 0
    for i in given:
        if i in actual:
            actual = list(actual)
            actual.remove(i)
            actual = ''.join(actual)
            score += 1
    return score/len(given)

async def create_page(client,ctx,embeds,files=None,starting=0,respond=False):
    print("Arguments Received Successfully")
    if files == None:
        files = [None]*len(embeds)
    cur_page = starting
    if respond == False:
        book = await ctx.send(embed=embeds[cur_page],file=files[cur_page])
    else:
        book = await ctx.respond(embed=embeds[cur_page],file=files[cur_page])

    while True:
        accepted_reactions = []
        if respond == False:
            print("Book is of type")
            await book.edit(embed=embeds[cur_page],file=files[cur_page])
        else:
            await book.edit_original_message(embed=embeds[cur_page],file=files[cur_page])
        if cur_page != 0:
            book.add_reaction("⬅️")
            accepted_reactions.append("⬅️")
        if cur_page != len(embeds)-1:
            book.add_reaction("➡️")
            accepted_reactions.append("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in accepted_reactions
        try:
            reaction, user = await client.wait_for("reaction_add", timeout = 600, check=check)
        except asyncio.TimeoutError:
            book.clear_reactions()
            return
        await book.remove_reaction(reaction, user)

        if str(reaction.emoji) == "⬅️": cur_page -= 1
        elif str(reaction.emoji) == "➡":    cur_page += 1


class InvalidArguments(Exception):
    pass

class Handler:
    def __init__(self):
        # self.connected_guilds = [583467562885709835, 695118970986168360, 782596986339328010, 788720078606434314, 820095117397721129, 828146605567377428, 833178704888463400, 855306849012285440, 876305527196516363]
        self.connected_guilds = [695118970986168360]
        self.supported_subjects_dict = {
            2236 : "Geography",
            2174 : "History",
            4048 : "Mathematics",
            4049 : "Additional Mathematics",
            6091 : "Physics",
            6092 : "Chemistry",
            6093 : "Biology",
            7155 : "Computing"
        }
        self.supported_subjects_text = "\n".join([f"{k} - {self.supported_subjects_dict[k]}" for k in self.supported_subjects_dict])

        self.contribute_message1 = "**We're So happy you would like to Help!!**\nDefine is in its __Development Stage__ and we currently accept support through donation of Content Notes and Questions in the form of Past-year papers or worksheets for the following Subjects: **Biology**, **Pure/Elect History**, **Social Studies**, **Pure/Elect Geography**, **Mathematics**\n__Do ensure that if the owner of the notes is not you, the piece of work is free of copyright restrictions.__\nContent Notes of *Substantial Quality* may be *consdered* for **purchase**\nDo Messsage <@!591107669180284928> for more information"

        self.legal_message1 = "**All information** about Syllabus including but not only Assessment Objectives, Topics Examined and Examination Settings are taken/adapted from the [Offical SEAB Website](https://www.seab.gov.sg/home/examinations/gce-o-level/o-level-syllabuses-examined-for-school-candidates-2022)\n\n**All Content information for subjects are given by volunteers who have donated their notes. Credit to Contributors of each Subject can be found using the `/credits` function**\n\n **Define** does not directly own information about the syllabus, but owns literal content for subjects written by contributors on behalf of the contributors, unless stated otherwise.\nIntellectual Property (defined as the uniqueness of the notes) of Define cannot be directly copied without being referenced, unless under Public Domain or stated otherwise.\n\nIf there are any discrepancies or flaw in information, do feel free to use the `/report` command describing the issue"

        # Assessment Objectives

        self._2174_ao = {
            "Deploy Knowledge":"Recall, select, organise and use historical knowledge in context.",
            "Construct Explanation and Communicate Historical Knowledge" : "Understanding of the past thourgh explanation and analysis of:\nCausation, consequence, continuity, change and significance within a historical context,\nKey features and characteristics of the periods studied and the relationship between them\nand their ability to evaluate causation and historical significance to arrive at a reasoned conclusion.",
            "Interpret and Evaluate Source Materials":"Understand, analyse and evaluate:\nA range of source materials as part of an historical enquiry,\n and how aspects of the past have been interpreted and represented in different ways through:\n- Comprehending and extracting relevant information\n- Drawing inferences from given information\n- Comparing and contrasting different views\n- Distinguishing between facts, opinion and judgement\n– Recognising values and detecting bias\n– Establishing utility of given information\n – Drawing conclusions based on a reasoned consideration of evidence and arguments."
        }

        self._2236_ao = {
            "Knowledge" : "demonstrate relevant factual knowledge – geographical facts, concepts, processes, interactions and trends\ndemonstrate knowledge of relevant fieldwork techniques – identification of geographical question,sequence of fieldwork inquiry, primary and secondary data collection methods",
            "Critical Understanding and Constructing Explanation" : "select, organise and apply concepts, terms and facts learnt\nmake judgements, recommendations and decisions\nevaluate data collection methods and suggest improvements ",
            "Interpreting and Evaluating Geographical Data " : "comprehend and extract relevant information from geographical data (numerical, diagrammatic, pictorial and graphical forms)\nuse and apply geographical knowledge and understanding to interpret geographical data\n– recognise patterns in geographical data and deduce relationships\n– compare and contrast different views\n– present geographical data in an appropriate form and in an effective manner\n– draw conclusions based on a reasoned consideration of evidence\nevaluate the validity and limitations of fieldwork evidence and of the conclusions reached"
        }

        self._4048_ao = {
            "Understand and Apply" : "understand and apply mathematical concepts and skills in a variety of contexts",
            "Organise and Analyse" : "Organise and analyse data and information; formulate and solve problems, including those in real-world contexts, by selecting and applying appropriate techniques of solution; interpret mathematical results",
            "Solve" : "solve higher order thinking problems; make inferences; write mathematical explanation and arguments"
        }

        self._4049_ao = {
            "Use and apply standard techniques" : "recall and use facts, terminology and notation\nread and use information directly from tables, graphs, diagrams and texts\nCarry out routine mathematical procedures",
            "Solve problems in a variety of contexts" : "interpret information to identify the relevant mathematics concept, rule or formula to use\ntranslate information from one form to another\nmake and use connections across topics/subtopics\nformulate problems into mathematical terms\nanalyse and select relevant information and apply appropriate mathematical techniques to solve problems\ninterpret results in the context of a given problem",
            "Reason and communicate mathematically" : "justify mathematical statements\nprovide explanation in the context of a given problem\nwrite mathematical arguments and proofs"
        }

        self._6091_ao = {
            "Knowledge with Understanding" : "Demonstrate knowledge and understanding in relation to:\n1. Scientific phenomena, facts, laws, definitions, concepts, theories\n2. Scientific vocabulary, terminology, conventions (including symbols, quantities and units)\n3. Scientific instruments and apparatus, including techniques of operation and aspects of safety\n4. Scientific quantities and their determination\n5. Scientific and technological applications with their social, economic and environmental implications.\n\nThe subject content defines the factual knowledge that candidates may be required to recall and explain.\nQuestions testing these objectives will often begin with one of the following words: define, state, describe, explain or outline.",
            "Handling Information and Solving Problems" : "Able (in words or by using symbolic, graphical and numerical forms of presentation) to:\n1. Locate, select, organise and present information from a variety of sources\n2. Translate information from one form to another\n3. Manipulate numerical and other data\n4. Use information to identify patterns, report trends and draw inferences\n5. Present reasoned explanations for phenomena, patterns and relationships\n6. Make predictions and propose hypotheses\n7. Solve problems.\n\nThese assessment objectives cannot be precisely specified in the subject content because questions testing such skills may be based on information which is unfamiliar to the candidate. In answering such questions, candidates are required to use principles and concepts that are within the syllabus and apply them in a logical, reasoned or deductive manner to a novel situation. Questions testing these objectives will often begin with one of the following words: predict, suggest, calculate or determine.",
            "Experimental Skills and Investigations" : "1. Follow a sequence of instructions\n2. Use techniques, apparatus and materials\n3. Make and record observations, measurements and estimates\n4. Interpret and evaluate observations and experimental results\n5. Plan investigations, select techniques, apparatus and materials\n6. evaluate methods and suggest possible improvements."
        }

        self._6092_ao = {
            "Knowledge with Understanding" : "Demonstrate knowledge and understanding in relation to:\n1. Scientific phenomena, facts, laws, definitions, concepts, theories\n2. Scientific vocabulary, terminology, conventions (including symbols, quantities and units)\n3. Scientific instruments and apparatus, including techniques of operation and aspects of safety\n4. Scientific quantities and their determination\n5. Scientific and technological applications with their social, economic and environmental implications.\n\nThe subject content defines the factual knowledge that candidates may be required to recall and explain.\nQuestions testing those objectives will often begin with one of the following words: define, state, describe, explain or outline",
            "Handling Information and Solving Problems" : "Able (in words or by using symbolic, graphical and numerical forms of presentation) to:\n1. Locate, select, organise and present information from a variety of sources\n2. Translate information from one form to another\n3. Manipulate numerical and other data\n4. Use information to identify patterns, report trends and draw inferences\n5. Present reasoned explanations for phenomena, patterns and relationships\n6. Make predictions and propose hypotheses\n7. solve problems.\n\nThese assessment objectives cannot be precisely specified in the subject content because questions testing these objectives may be based on information which is unfamiliar to the candidates. In answering such questions, candidates are required to use principles and concepts that are within the syllabus and apply them in a logical, reasoned or deductive manner to a novel situation. Questions testing these objectives will often begin with one of the following words: predict, deduce, suggest, calculate or determine",
            "Experimental Skills and Investigations" : "Able to:\n1. follow a sequence of instructions\n2. use techniques, apparatus and materials\n3. make and record observations, measurements and estimates\n4. interpret and evaluate observations and experimental results\n5. plan investigations, select techniques, apparatus and materials\n6. evaluate methods and suggest possible improvements."
         }

        self._6093_ao = {
            "Knowledge with Understanding" : "Demonstrate knowledge and understanding in relation to:\nScientific phenomena, facts, laws, definitions, concepts, theories\nScientific vocabulary, terminology, conventions (including symbols, quantities and units)\nScientific instruments and apparatus, including techniques of operation and aspects of safety\nScientific quantities and their determination\nScientific and technological applications with their social, economic and environmental implications.\n\nThe subject content defines the factual knowledge that candidates may be required to recall and explain.\nQuestions testing those objectives will often begin with one of the following words: define, state, describe,explain or outline.",
            "Handling Information and Solving Problems" : "Able – in words or by using symbolic, graphical and numerical forms of presentation – to:\nLocate, select, organise and present information from a variety of sources\nTranslate information from one form to another\nManipulate numerical and other data\nUse information to identify patterns, report trends and draw inferences\nPresent reasoned explanations for phenomena, patterns and relationships\nMake predictions and propose hypotheses\nSolve problems.",
            "Experimental Skills and Investigations" : "Able to:\nFollow a sequence of instructions\nUse techniques, apparatus and materials\nMake and record observations, measurements and estimates\nInterpret and evaluate observations and experimental results\nPlan investigations, select techniques, apparatus and materials\nEvaluate methods and suggest possible improvements."
        }

        self._7155_ao = {
            "Knowledge and Understanding" : "Knowledge and understanding of basic computing technology and systems, concepts, algorithms, techniques and tools.",
            "Applciation" : "Application of knowledge and understanding to analyse and solve computing problems",
            "Development" : "Development, testing and refinement of solutions using appropriate software application(s) and/or programming language(s)."
        }
        # Syllabus

        self._2236_syllabus_overview = {
            "Theme 1: Our Dynamic Planet (Physical Geography)" : "(1) Coasts – Should coastal environments matter?\n(2) Living with Tectonic Hazards – Risk or opportunity?\n(3) Variable Weather and Changing Climate – A continuing challenge?",
            "Theme 2: Our Changing World (Human Geography)" : "(4) Global Tourism – Is tourism the way to go?\n(5) Food Resources – Is technology a panacea for food shortage?\n(6) Health and Diseases – Are we more vulnerable than before?",
            "Theme 3: Geographical Skills and Investigations" : "(7) Topographical Map Reading Skills\n(8) Geographical Data and Techniques\n(9) Geographical Investigations"
        }

        self._4048_syllabus_overview = {
            "N1" : "Numbers and their operations",
            "N2" : "Ratio and proportion",
            "N3" : "Percentage",
            "N4" : "Rate and speed",
            "N5" : "Algebraic expressions and formulae",
            "N6" : "Functions and graphs",
            "N7" : "Equations and inequalities",
            "N8" : "Set language and notation",
            "N9" : "Matrices",
            "N10" : "Problems in real-world contexts",
            "G1" : "Angles, triangles and polygons",
            "G2" : "Congruence and similarity",
            "G3" : "Properties of circles",
            "G4" : "Pythagoras’ theorem and trigonometry",
            "G5" : "Mensuration",
            "G6" : "Coordinate geometry",
            "G7" : "Vectors in two dimensions",
            "G8" : "Problems in real-world contexts",
            "S1" : "Data analysis",
            "S2" : "Probability"
        }

        self._2174_syllabus_overview = {
            "Unit 1" : "European Dominance and Expansion in the late 19th century",
            "Unit 2" : "The World in Crisis",
            "Unit 3" : "Bi-Polarity and the Cold War",
            "Unit 4" : "Decolonisation and Emergence of Nation-States"
        }

        self._4049_syllabus_overview = {
            "A1" : "Quadratic functions",
            "A2" : "Equations and inequalities",
            "A3" : "Surds",
            "A4" : "Polynomials and partial fractions",
            "A5" : "Binomial expansions",
            "A6" : "Exponential and logarithmic functions",
            "G1" : "Trigonometric functions, identities and equations",
            "G2" : "Coordinate geometry in two dimensions",
            "G3" : "Proofs in plane geometry",
            "C1" : "Differentiation and integration"
        }

        self._6091_syllabus_overview = {
            "Measurements" : "Physical Quantities, Units and Measurement",
            "Newtonian Mechanics" : "Kinematics\nDynamics\nMass, Weight and Density\nTurning Effect of Forces\nPressure\nEnergy, Work and Power",
            "Thermal Physics" : "Kinetic Model of Matter\nTransfer of Thermal Energy\nTemperature\nThermal Properties of Matter",
            "Waves" : "General Wave Properties\nLight\nElectromagnetic Spectrum\nSounds",
            "Electricity and Magnetism" : "Static Electricity\nCurrent of Electricity\nD.C. Circuits\nPractical Electricity\nMagnetism\nElectromagnetism\nElectromagnetic Induction "
        }

        self._6092_syllabus_overview = {
            "Experimental Chemistry" : "Experimental Chemistry",
            "Atomic Structure And Stoichiometry" : "The Particulate Nature of Matter\nFormulae, Stoichiometry and the Mole Concept",
            "Chemistry Of Reactions" : "Electrolysis\nEnergy from Chemicals\nChemical Reactions\nAcids, Bases and Salts",
            "Periodicity" : "The Periodic Table\nMetals",
            "Atmosphere" : "Air",
            "Organic Chemistry" : "Organic Chemistry"
        }

        self._6093_syllabus_overview = {
            "Principles Of Biology" : "Cell Structure and Organisation\nMovement of Substances\nBiological Molecules",
            "Maintenance And Regulation Of Life Processes " : "Nutrition in Humans\nNutrition in Plants\nTransport in Flowering Plants\nTransport in Humans\nRespiration in Humans\nExcretion in Humans\nHomeostasis\nCo-ordination and Response in Humans",
            "Continuity Of Life" : "Reproduction\nCell Division\nMolecular Genetics\nInheritance",
            "Man And His Environment" : "Organisms and their Environment"
        }

        self._7155_syllabus_overview = {
            "Module 1 - Data And Information" : "This module is about the handling and processing of data in computer systems, and the need to be ethical when dealing with data. Students should be able to identify different types of data, understand and explain what the data is for, and explain how the data is represented or organised for processing and output with reference to a given problem. Students will be more aware of ethical issues with respect to data, including privacy of data.",
            "Module 2 – Systems And Communications " : "This module is about systems involving computer technology and computing devices. Students will learn the inter-relationships between parts and whole of a system; as well as the functions of parts of systems in enabling communications between human and computing device (machine), machine and machine, and within a machine. ",
            "Module 3 – Abstraction And Algorithms" : "This module is about problem solving and how a problem may be solved by breaking it into smaller, manageable parts and solving all the smaller parts. An algorithm describes a solution for the problem that is independent of a programming language and may be presented in pseudo-code (where program structures will be more pronounced) or diagrammatically (flowchart). Students should be able to know the difference between pseudo-code and flowchart.",
            "Module 4 - Programming " : "This module is about application and development of logical thinking and reasoning, as well as problem-solving skills through the design and development of software solutions using programming language(s). An algorithm describes a solution independent of a programming language while a programming language depicts the solution that is workable on a computing device."
        }

        # Topic Details

        raw_json = json.load(open(r"resources/topic_details.json"))
        self.topic_desc = raw_json
        self.all_topics = [f"{subj} | {sub_topic}" for subj in raw_json for sub_topic in raw_json[subj]]

    def fuzzy_search_subject(self,query):
        if query in list(map(str,self.supported_subjects_dict.keys())):
            return int(query),self.supported_subjects_dict[int(query)]
        elif query.isdigit():
            return None,None
        matches = {key:match(query,self.supported_subjects_dict[key]) for key in self.supported_subjects_dict}
        best_match = [i for i in matches if matches[i]==max([matches[n] for n in matches])]
        return best_match[0],self.supported_subjects_dict[best_match[0]]

    @classmethod
    def create_embed(cls,elements):
        embed = None
        desc = ""
        file = None

        for element in elements:
            name = list(element.keys())[0]
            if "text" == name:
                desc += element[name]
            elif "bold" == name:
                desc += f"**{element[name]}**"
            elif "italics" == name:
                desc += f"*{element[name]}*"
            elif "code" == name:
                desc += f"```\n{element[name]}\n```"
            elif "underline" == name:
                desc += f"__\n{element[name]}\n__"
            elif "quote" == name:
                desc += f"> {element[name]}"
            else:
                continue
            desc += "\n\n"

        for element in elements:
            name = list(element.keys())[0]
            if "title" == name:
                embed = discord.Embed(
                    title = element[name],
                    description = desc,
                    colour = discord.Colour.random()
                )
                break
        else:
            embed = discord.Embed(
                description = desc,
                colour = discord.Colour.random()
            )

        for element in elements:
            name = list(element.keys())[0]
            if "image" in name:
                if name == "local-image":
                    file = discord.File(element[name],filename="image.jpg")
                    embed.set_image(url=f"attachment://image.jpg")
                else:
                    embed.set_image(url=element[name])
            elif "thumbnail" == name:
                embed.set_thumbnail(url=element[name])
            elif "footer" == name:
                embed.set_footer(text=element[name])
            else:
                continue
        return embed,file
