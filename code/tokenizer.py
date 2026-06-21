import json
import os
import re
import difflib

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
        # 0-9: Generic LLM Tokens
        self._add_token(0, "<PAD>", None)
        self._add_token(1, "<BOS>", None)
        self._add_token(2, "<EOS>", None)
        self._add_token(5, "<UNKNOWN_WORD>", "unknown word")
        
        # 10-29: Modes
        self._add_token(10, "<FACT>", "fact")
        self._add_token(11, "<QUERY>", "query")
        self._add_token(12, "<STATE>", None)
        self._add_token(13, "<ANSWER>", "answer")
        self._add_token(14, "<BATTLE>", None)
        
        # 30-99: General Grammar and Logic
        self._add_token(30, "<TURN>", "Turn")
        self._add_token(31, "<HP_REMAINING>", "HP remaining.")
        self._add_token(32, "<FAINTED>", "fainted.")
        self._add_token(33, "<BATTLE_WON>", "won.")
        self._add_token(34, "<BATTLE_LOST>", "lost.")
        self._add_token(35, "<HAS>", "has")
        self._add_token(36, "<IS>", "is")
        self._add_token(37, "<TYPE>", "type")
        self._add_token(38, "<ACTION_USE>", "used")
        self._add_token(39, "<TARGET_AGAINST>", "against")
        self._add_token(40, "<TARGET_ON>", "on")
        self._add_token(41, "<EFFECT_SUPER>", "It was super effective.")
        self._add_token(42, "<EFFECT_NORMAL>", "It was effective.")
        self._add_token(43, "<EFFECT_WEAK>", "It was not very effective.")
        self._add_token(44, "<EFFECT_NONE>", "It had no effect.")
        self._add_token(64, "<EFFECT_MUTUAL_FAINT>", "both pokemon exhausted themselves and fainted.")
        self._add_token(45, "<BASE_HP>", "base hp")
        self._add_token(46, "<EVOLVES_INTO>", "evolves into")
        self._add_token(47, "<POWER>", "power")
        self._add_token(48, "<OBTAINED_FROM>", "obtained from")
        self._add_token(49, "<EFFECT_FELL_ASLEEP>", "fell asleep.")
        self._add_token(50, "<EFFECT_FAST_ASLEEP>", "is fast asleep.")
        self._add_token(51, "<EFFECT_HURT_BIND>", "is hurt by bind.")
        self._add_token(52, "<EFFECT_RESTORED_SLEEP>", "went to sleep and restored its hp.")
        self._add_token(53, "<EFFECT_MISSED>", "It missed!")
        self._add_token(54, "<TARGET_ITSELF>", "on itself.")
        
        # V2 Grammar Tokens
        self._add_token(55, "<PLAYER>", "player")
        self._add_token(56, "<LEADER>", "leader")
        self._add_token(57, "<WITHDREW>", "withdrew")
        self._add_token(58, "<SENT_OUT>", "sent out")
        
        # Prefix Grammar Tokens
        self._add_token(80, "<PLAYER_VS_LEADER>", "player vs leader.")
        self._add_token(81, "<HAS_1_LEFT>", "has one pokemon left.")
        self._add_token(82, "<HAS_2_LEFT>", "has two pokemon left.")
        self._add_token(83, "<HAS_3_LEFT>", "has three pokemon left.")
        self._add_token(84, "<VS>", "vs")
        self._add_token(85, "<LEADER>", "leader")
        self._add_token(70, "<LOGIC_AND>", "logic_and")
        self._add_token(71, "<LOGIC_OR>", "logic_or")
        self._add_token(72, "<LOGIC_NOT>", "logic_not")
        self._add_token(63, "<HAS_MOVES>", "has moves")
        self._add_token(73, "<LOGIC_TRUE>", "logic_true")
        self._add_token(74, "<LOGIC_FALSE>", "logic_false")
        self._add_token(75, "<LOGIC_LPAREN>", "logic_lparen")
        self._add_token(76, "<LOGIC_RPAREN>", "logic_rparen")
        self._add_token(86, "<AND>", "and")
        
        # 100-199: Types
        self._add_token(199, "<UNKNOWN_POWER>", "unknown power")
        self._add_token(100, "<UNKNOWN_TYPE>", "unknown type")
        self._add_token(196, "<TYPE_DARK>", "dark")
        self._add_token(197, "<TYPE_FAIRY>", "fairy")
        self._add_token(198, "<TYPE_STEEL>", "steel")
        with open(os.path.join(self.data_dir, "type_chart.json"), "r", encoding="utf-8") as f:
            type_chart = json.load(f)
            
        types = list(type_chart.keys())
        for i, t in enumerate(types):
            self._add_token(101 + i, f"<TYPE_{t.upper()}>", t)
        
        # 200-999: MOVES
        self._add_token(200, "<UNKNOWN_MOVE>", "unknown move")
        with open(os.path.join(self.data_dir, "moves.json"), "r", encoding="utf-8") as f:
            moves = json.load(f)
            
        for i, move in enumerate(moves.keys()):
            formatted_move = move.upper().replace(" ", "_")
            self._add_token(201 + i, f"<MOVE_{formatted_move}>", move)
            
        # 900-999: Locations and Encounters
        self._add_token(900, "<ENC_UNOBTAINABLE_WILD>", "unobtainable wild")
        self._add_token(901, "<ENC_COMMON_WILD>", "common wild")
        self._add_token(902, "<ENC_UNCOMMON_WILD>", "uncommon wild")
        self._add_token(903, "<ENC_RARE_WILD>", "rare wild")
        self._add_token(904, "<ENC_LEGENDARY>", "legendary")
        self._add_token(910, "<ENC_GIFT>", "gift")
        self._add_token(911, "<ENC_FISHING>", "fishing")
        self._add_token(912, "<ENC_FOSSIL>", "fossil")
        self._add_token(913, "<ENC_EVOLUTION>", "evolution")
        self._add_token(914, "<ENC_HATCHABLE>", "hatchable")
        self._add_token(915, "<ATTACKER>", "attacker")
        self._add_token(916, "<TARGET>", "target")
            
        # 1000+: POKEMON
        self._add_token(1000, "<UNKNOWN_PKMN>", "unknown pokemon")
        
        all_pokemon = []
        gen1_path = os.path.join(self.data_dir, "gen1_pokedex.json")
        gen2_path = os.path.join(self.data_dir, "gen2_pokedex.json")
        
        if os.path.exists(gen1_path):
            with open(gen1_path, "r", encoding="utf-8") as f:
                all_pokemon.extend(list(json.load(f).keys()))
        if os.path.exists(gen2_path):
            with open(gen2_path, "r", encoding="utf-8") as f:
                all_pokemon.extend(list(json.load(f).keys()))
        
        for i, pkmn in enumerate(all_pokemon):
            formatted_pkmn = pkmn.upper().replace(" ", "_").replace("♀", "F").replace("♂", "M")
            # 1000 + Pokedex Index (1-indexed)
            self._add_token(1001 + i, f"<PKMN_{formatted_pkmn}>", pkmn)
            if pkmn == "NidoranF":
                self.str_to_id["nidoran ♀"] = 1001 + i
                self.str_to_id["nidoran f"] = 1001 + i
                self.str_to_id["nidoran"] = 1001 + i
            if pkmn == "NidoranM":
                self.str_to_id["nidoran ♂"] = 1001 + i
                self.str_to_id["nidoran m"] = 1001 + i

        # 2000+: Bucketed Numbers (-100 to 500)
        idx = 2000
        for val in range(-100, 510, 10):
            self._add_token(idx, f"<{val}>", str(val))
            idx += 1
            
        # Precompile regexes for fast lookup
        self.search_terms = sorted(self.str_to_id.keys(), key=len, reverse=True)
        self.search_patterns = []
        for term in self.search_terms:
            if "♀" in term or "♂" in term or term.endswith(".") or term.endswith("!"):
                pattern = re.compile(re.escape(term))
            else:
                pattern = re.compile(r'\b' + re.escape(term) + r'\b')
            self.search_patterns.append((term, pattern))

    def export_vocab(self, filepath="vocab.json"):
        """Exports the vocabulary mapping for HuggingFace compatibility."""
        vocab = {tag: id for tag, id in sorted(self.tag_to_id.items(), key=lambda item: item[1])}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vocab, f, indent=4)
        print(f"Exported {len(vocab)} tokens to {filepath}")

    def encode_text(self, text, mode=None):
        """Translates free text into a list of Token IDs."""
        # Replace logic symbols and uppercase operators before lowercasing
        text = text.replace("(", "logic_lparen ")
        text = text.replace(")", " logic_rparen")
        
        # We replace whole words to avoid replacing substrings
        text = re.sub(r'\bAND\b', 'logic_and', text)
        text = re.sub(r'\bOR\b', 'logic_or', text)
        text = re.sub(r'\bNOT\b', 'logic_not', text)
        
        # True and False map to logic versions regardless of case
        text = re.sub(r'(?i)\btrue\b', 'logic_true', text)
        text = re.sub(r'(?i)\bfalse\b', 'logic_false', text)
        
        text = text.lower()
        
        # Strip out encounter numbers used for visual grouping
        text = re.sub(r'\s*\(encounter \d+\)', '', text)
        
        # Replace leader names with "leader" so they alias to the <LEADER> token and prefix rules
        leader_names = ["gary oak", "brock", "misty", "lieutenant surge", "erika", "koga", "sabrina", "blaine", "giovanni", "lorelei", "bruno", "agatha", "lance", "rival"]
        for name in leader_names:
            text = text.replace(name, "leader")
            
        token_ids = []
        
        # Convert all numbers to bucketed representations so they map naturally to vocab
        text = re.sub(r'(?<!\w)-?\d+\b', lambda m: str(int(round(int(m.group()) / 10.0)) * 10), text)
        
        # 1. ALWAYS start with <BOS>
        token_ids.append(1)
        
        # 2. Add mode token if provided
        if mode and f"<{mode}>" in self.tag_to_id:
            token_ids.append(self.tag_to_id[f"<{mode}>"])
            
        # Find all occurrences using precompiled patterns
        matches = []
        for term, pattern in self.search_patterns:
            for m in pattern.finditer(text):
                matches.append((m.start(), len(term), self.str_to_id[term]))
                    
        # Remove overlaps (keep longest match first)
        # Sort by start position (ascending), then by term length (descending)
        matches.sort(key=lambda x: (x[0], -x[1]))
        
        filtered_matches = []
        last_end = -1
        
        # Track which characters are "covered" by known tokens
        covered = [False] * len(text)
        
        for match in matches:
            start_pos = match[0]
            term_len = match[1]
            term_id = match[2]
            
            if start_pos >= last_end:
                filtered_matches.append((start_pos, term_id))
                last_end = start_pos + term_len
                for i in range(start_pos, last_end):
                    if i < len(covered):
                        covered[i] = True
                        
        # Find unknown words (alphabetic characters not covered)
        unknown_id = self.tag_to_id.get("<UNKNOWN_WORD>", 5)
        for m in re.finditer(r'\b[a-z_]+\b', text):
            start_pos = m.start()
            word = m.group()
            if not covered[start_pos]:
                if word == "hp":
                    filtered_matches.append((start_pos, self.tag_to_id.get("<HP_REMAINING>", unknown_id)))
                else:
                    closest = difflib.get_close_matches(word, self.search_terms, n=1, cutoff=0.75)
                    if closest:
                        filtered_matches.append((start_pos, self.str_to_id[closest[0]]))
                    else:
                        raise ValueError(f"Unknown word detected during tokenization: '{word}' in text: '{text}'")
                
        # Sort again by start_pos so unknown words are interleaved correctly
        filtered_matches.sort()
        
        # Append to our sequence
        for match in filtered_matches:
            token_ids.append(match[1])
            
        # 3. ALWAYS end with <EOS>
        token_ids.append(2)
            
        return token_ids

    def decode_to_tags(self, token_ids):
        """Converts token IDs to their structural DSL string tags."""
        tags = []
        for t in token_ids:
            tags.append(self.id_to_tag.get(t, "<UNKNOWN>"))
        return tags

    def decode_to_text(self, token_ids):
        """Converts token IDs to human-readable game text."""
        parts = []
        for t in token_ids:
            if t == 1 or t == 2: # Ignore BOS/EOS
                continue
            if t in self.id_to_str and self.id_to_str[t] is not None:
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
