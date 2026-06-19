import json
import os
import re

class PokemonTokenizer:
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        else:
            self.data_dir = data_dir
            
        self.str_to_id = {}
        self.id_to_str = {}
        
        self.tag_to_id = {}
        self.id_to_tag = {}
        
        self._build_vocab()
        
    def _add_token(self, token_id, token_tag, string_repr):
        self.tag_to_id[token_tag] = token_id
        self.id_to_tag[token_id] = token_tag
        
        if string_repr:
            # lowercased for free text matching
            self.str_to_id[string_repr.lower()] = token_id
            self.id_to_str[token_id] = string_repr

    def _build_vocab(self):
        # 0-99: MODE, TYPES, ACTIONS
        # 0: UNKNOWN_TYPE
        self._add_token(0, "<UNKNOWN_TYPE>", "unknown type")
        
        # 1-9: MODE TOKENS
        self._add_token(1, "<FACT>", None)
        self._add_token(2, "<QUERY>", None)
        self._add_token(3, "<STATE>", None)
        self._add_token(4, "<ANSWER>", None)
        
        # 10-29: TYPES
        with open(os.path.join(self.data_dir, "type_chart.json"), "r", encoding="utf-8") as f:
            type_chart = json.load(f)
            
        types = list(type_chart.keys())
        for i, t in enumerate(types):
            self._add_token(10 + i, f"<TYPE_{t.upper()}>", t)
            
        # 30-49: ACTIONS AND EFFECTS
        self._add_token(30, "<ACTION_USE>", "used")
        self._add_token(31, "<TARGET_AGAINST>", "against")
        self._add_token(32, "<TARGET_ON>", "on")
        self._add_token(33, "<EFFECT_SUPER>", "It was super effective.")
        self._add_token(34, "<EFFECT_NORMAL>", "It was effective.")
        self._add_token(35, "<EFFECT_WEAK>", "It was not very effective.")
        self._add_token(36, "<EFFECT_NONE>", "It had no effect.")
        
        # 50-69: BATTLE STATE
        self._add_token(50, "<TURN>", "Turn")
        self._add_token(51, "<HP_REMAINING>", "HP remaining.")
        self._add_token(52, "<FAINTED>", "fainted.")
        self._add_token(53, "<BATTLE_WON>", "won.")
        self._add_token(54, "<BATTLE_LOST>", "lost.")
        
        # 70-89: LOGIC
        self._add_token(70, "<LOGIC_AND>", "and")
        self._add_token(71, "<LOGIC_OR>", "or")
        self._add_token(72, "<LOGIC_NOT>", "not")
        
        # 100-999: MOVES
        self._add_token(100, "<UNKNOWN_MOVE>", "unknown move")
        with open(os.path.join(self.data_dir, "moves.json"), "r", encoding="utf-8") as f:
            moves = json.load(f)
            
        for i, move in enumerate(moves.keys()):
            formatted_move = move.upper().replace(" ", "_")
            self._add_token(101 + i, f"<MOVE_{formatted_move}>", move)
            
        # 1000+: POKEMON
        self._add_token(1000, "<UNKNOWN_PKMN>", "unknown pokemon")
        
        GEN1_POKEMON = [
            "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", 
            "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", 
            "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran ♀", "Nidorina", "Nidoqueen", 
            "Nidoran ♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", 
            "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", 
            "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", 
            "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", 
            "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", 
            "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", 
            "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", 
            "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", 
            "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", 
            "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", 
            "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", 
            "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"
        ]
        
        for i, pkmn in enumerate(GEN1_POKEMON):
            formatted_pkmn = pkmn.upper().replace(" ", "_").replace("♀", "F").replace("♂", "M")
            # 1000 + Pokedex Index (1-indexed)
            self._add_token(1001 + i, f"<PKMN_{formatted_pkmn}>", pkmn)

    def export_vocab(self, filepath="vocab.json"):
        """Exports the vocabulary mapping for HuggingFace compatibility."""
        vocab = {tag: id for tag, id in self.tag_to_id.items()}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vocab, f, indent=4)
        print(f"Exported {len(vocab)} tokens to {filepath}")

    def encode_text(self, text, mode="QUERY"):
        """Translates free text into a list of Token IDs."""
        text = text.lower()
        token_ids = []
        
        # Add mode token
        if f"<{mode}>" in self.tag_to_id:
            token_ids.append(self.tag_to_id[f"<{mode}>"])
            
        # Very simple greedy extraction parser (longest match first)
        # We sort by length descending so "Water Gun" matches before "Water"
        search_terms = sorted(self.str_to_id.keys(), key=len, reverse=True)
        
        # Find all occurrences
        matches = []
        for term in search_terms:
            for m in re.finditer(r'\b' + re.escape(term) + r'\b', text):
                matches.append((m.start(), self.str_to_id[term]))
                
            # Handle special characters like Nidoran female
            if "♀" in term or "♂" in term:
                for m in re.finditer(re.escape(term), text):
                    matches.append((m.start(), self.str_to_id[term]))
                    
            # Handle punctuation marks from effects
            if term.endswith("."):
                for m in re.finditer(re.escape(term), text):
                    matches.append((m.start(), self.str_to_id[term]))
                    
        # Match numbers for 5000+ IDs
        for m in re.finditer(r'\b\d+\b', text):
            matches.append((m.start(), 5000 + int(m.group())))
        
        # Remove overlaps (keep longest)
        matches.sort()
        filtered_matches = []
        last_end = -1
        
        for match in matches:
            start_pos = match[0]
            term_id = match[1]
            if term_id >= 5000:
                term_len = len(str(term_id - 5000))
            else:
                term_len = len(self.id_to_str[term_id])
            
            if start_pos >= last_end:
                filtered_matches.append(match)
                last_end = start_pos + term_len
                
        # Append to our sequence
        for match in filtered_matches:
            token_ids.append(match[1])
            
        return token_ids

    def decode_to_tags(self, token_ids):
        """Converts token IDs to their structural DSL string tags."""
        tags = []
        for t in token_ids:
            if t >= 5000:
                tags.append(f"<{t - 5000}>")
            else:
                tags.append(self.id_to_tag.get(t, "<UNKNOWN>"))
        return tags

    def decode_to_text(self, token_ids):
        """Converts token IDs to human-readable game text."""
        parts = []
        for t in token_ids:
            if t >= 5000:
                parts.append(str(t - 5000))
            elif t in self.id_to_str and self.id_to_str[t] is not None:
                # Capitalize Pokemon/Moves
                s = self.id_to_str[t]
                if t >= 1000 or (t >= 100 and t <= 999):
                    s = s.title()
                parts.append(s)
                
        # Simple cleanup for punctuation
        raw_text = " ".join(parts)
        raw_text = raw_text.replace(" .", ".")
        # Fix casing for start of sentences
        sentences = raw_text.split(". ")
        sentences = [s.capitalize() for s in sentences if s]
        return ". ".join(sentences)

if __name__ == "__main__":
    tokenizer = PokemonTokenizer()
    tokenizer.export_vocab("vocab.json")
    
    # Test encoding
    free_text = "Have Charmander use Ember against the grass type. It was super effective."
    print(f"\n[Test] Input text: '{free_text}'")
    
    ids = tokenizer.encode_text(free_text, mode="STATE")
    print(f"[Test] Token IDs: {ids}")
    
    tags = tokenizer.decode_to_tags(ids)
    print(f"[Test] Tags: {tags}")
    
    output_text = tokenizer.decode_to_text(ids)
    print(f"[Test] Detokenized text: '{output_text}'")
    
    # Test a raw game string
    game_string = "Bulbasaur used Tackle against Onix. It was not very effective."
    print(f"\n[Test] Input game string: '{game_string}'")
    ids2 = tokenizer.encode_text(game_string, mode="FACT")
    print(f"[Test] Token IDs: {ids2}")
    tags2 = tokenizer.decode_to_tags(ids2)
    print(f"[Test] Tags: {tags2}")
    out2 = tokenizer.decode_to_text(ids2)
    print(f"[Test] Detokenized text: '{out2}'")
