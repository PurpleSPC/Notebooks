        # mark  the cell as a move thats been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # list the neighbors of the cell
        neighbors = self.list_unknown_neighbors(cell)

        # add to knowledge based on cell's count
        new_sentence = Sentence(cells=neighbors, count=count)
        self.knowledge.append(new_sentence)

        # mark any additional cells as safe or as mines if possible
        for sentence in self.knowledge:
            # known safe
            if len(sentence.cells) > 0 and sentence.count == 0:
                for cell in sentence.cells:
                    self.mark_safe(cell)
            # known mines
            if len(sentence.cells) > 0 and len(sentence.cells) == sentence.count:
                for cell in sentence.cells:
                    self.mark_mine(cell)
        
        # Add any new sentences to KB if they can be inferred
        for sentence in self.knowledge:
            for cell in sentence.cells:
                # remove known safes from existing sentences
                if cell in self.safes:
                    sentence.mark_safe(cell)
                # remove known mines from existing sentences
                if cell in self.mines:
                    sentence.mark_mine(cell)

                
