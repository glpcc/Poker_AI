from __future__ import annotations
from dataclasses import dataclass
from math import comb
from functools import reduce
from itertools import product
CARD_VALUES = {
    "2":1,
    "3":2,
    "4":3,
    "5":4,
    "6":5,
    "7":6,
    "8":7,
    "9":8,
    "10":9,
    "J":10,
    "Q":11,
    "K":12,
    "A":13
}
COLORS = ['S','H','D','C']
HAND_TYPES = {
    "Straight Flush":0,
    "Royal Flush":1,
    "Poker":2,
    "Full House":3,
    "Flush":4,
    "Straight":5,
    "Triples":6,
    "Double Pairs":7,
    "Pairs":8,
    "High Card":9
}
TOTAL_CARDS = 52
# Test to try to start to program the game
@dataclass
class Card():
    color: str
    value: str

    def __ge__(self, other: Card) -> bool:
        return CARD_VALUES[self.value] >= CARD_VALUES[other.value]

    def __le__(self, other: Card) -> bool:
        return CARD_VALUES[self.value] <= CARD_VALUES[other.value]

    def __gt__(self, other: Card) -> bool:
        return CARD_VALUES[self.value] > CARD_VALUES[other.value]

    def __lt__(self, other: Card) -> bool:
        return CARD_VALUES[self.value] < CARD_VALUES[other.value]

    def __repr__(self) -> str:
        return f'{self.value}{self.color}'



class Hand():
    def __init__(self,hand_type: str,cards: list[Card]) -> None:
        self.type = hand_type
        self.cards = cards
    
    def custom_compare(self,l: list[int]) -> bool:
        print(l)
        for i in range(0,len(l),2):
            if l[i] > l[i+1]:
                return True
            elif l[i] < l[i+1]:
                return False
        return False

    def compare_pos(self,other_hand: Hand,pos: list[int]):
        l = []
        for i in pos:
            if i < len(self.cards):
                l.append(CARD_VALUES[self.cards[i].value])
                l.append(CARD_VALUES[other_hand.cards[i].value])
        return self.custom_compare(l)
    
    def __eq__(self, other: Hand) -> bool:
        if self.type != other.type:
            return False
        if self.type == "Straight Flush" or self.type == "Straight":
            return self.cards[0].value == other.cards[0].value
        elif self.type == "Poker":
            return all(self.cards[i].value == other.cards[i].value for i in [0,4] if i < len(self.cards))
        elif self.type == "Full House":
            return self.cards[0].value == other.cards[0].value and self.cards[3].value == other.cards[3].value
        elif self.type == "Flush" or self.type == "High Card":
            return all(i.value == j.value for i,j in zip(self.cards,other.cards))
        elif self.type == "Triples":
            return all(self.cards[i].value == other.cards[i].value for i in [0,3,4] if i < len(self.cards))
        elif self.type == "Double Pairs":
            return all(self.cards[i].value == other.cards[i].value for i in [0,2,4] if i < len(self.cards))
        elif self.type == "Pairs":
            return all(self.cards[i].value == other.cards[i].value for i in [0,2,3,4] if i < len(self.cards))
        else:
            # Royal Flush
            return True

    def __gt__(self,other: Hand)-> bool:
        if self.type != other.type:
            return HAND_TYPES[self.type] > HAND_TYPES[other.type]
        if self.type == "Straight Flush" or self.type == "Straight":
            return self.compare_pos(other,[0])
        elif self.type == "Poker":
            return self.compare_pos(other,[0,4])
        elif self.type == "Full House":
            return self.compare_pos(other,[0,3])
        elif self.type == "Flush" or self.type == "High Card":
            return self.compare_pos(other,[0,1,2,3,4])
        elif self.type == "Straight":
            return self.compare_pos(other,[0])
        elif self.type == "Triples":
            return self.compare_pos(other,[0,3,4])
        elif self.type == "Double Pairs":
            return self.compare_pos(other,[0,2,4])
        elif self.type == "Pairs":
            return self.compare_pos(other,[0,2,3,4])
        else:
            # Royal Flush
            return False
    
    def __lt__(self,other: Hand)-> bool:
        return not self > other

    def __ge__(self,other: Hand)-> bool:
        return self == other or self > other
    
    def __le__(self,other: Hand)-> bool:
        return self == other or self < other
    
    def __repr__(self) -> str:
        return f'Hand(Hand_type: {self.type},Cards: {self.cards})'

def multiply_list(l):
    return reduce(lambda k,j: k*j,l,1)

def get_best_hand(cards: list[Card])-> Hand:
    hand = []
    # Count the number of values and color to check for pairs,triples,pokers or colors
    colors_nums: dict[str,list[Card]] = dict()
    value_nums: dict[str,list[Card]] = dict()
    for i in cards:
        if i.value in value_nums:
            value_nums[i.value].append(i)
        else:
            value_nums[i.value] = [i]
        
        if i.color in colors_nums:
            colors_nums[i.color].append(i)
        else:
            colors_nums[i.color] = [i]
        


    # Check for straights
    sorted_cards = sorted(cards, reverse=True)
    last_card = sorted_cards[0]
    straigth = [sorted_cards[0]]
    straights: list[list[Card]] = []
    for i in sorted_cards[1:]:
        if CARD_VALUES[last_card.value] - CARD_VALUES[i.value] == 1:
            straigth.append(i)
        else:
            straigth = [i]
        if len(straigth) == 5:
            straights.append(straigth)
            straigth = straigth[1:]
        last_card = i
    if len(straights) > 0:
        straight_flushes = [i for i in straights if all(j.color == i[0].color for j in i)]
        if len(straight_flushes) > 0:
            hand_type = "Straight Flush"
            hand = straight_flushes[0]
            if hand[0].value == 'A':
                hand_type = "Royal Flush"
            return Hand(hand_type,hand)

    triples = []
    pairs = []
    individuals = []
    pokers = []
    for i in value_nums:
        if len(value_nums[i]) == 1:
            individuals.append(value_nums[i][0])
        elif len(value_nums[i]) == 2:
            pairs.append(value_nums[i])
        elif len(value_nums[i]) == 3:
            triples.append(value_nums[i])
        else:
            pokers.append(value_nums[i])
    individuals = sorted(individuals,reverse=True)

    if len(pokers) > 0:
        hand_type = "Poker"
        hand = sorted(pokers,key= lambda k: k[0], reverse=True)[0]
        if len(cards) > 4:
            hand.append(individuals[0])
        return Hand(hand_type,hand)

    pairs = sorted(pairs,key= lambda k: k[0], reverse=True)
    triples = sorted(triples,key= lambda k: k[0], reverse=True)
    if len(triples) > 0 and len(pairs) > 0:
        hand_type = "Full House" 
        hand = triples[0] + pairs[0]
        return Hand(hand_type,hand)
    
    # WARNING no comparison between flushes is made cause no more than 7 cards are expected
    flushes = [colors_nums[i] for i in colors_nums if len(colors_nums[i])>=5]
    if len(flushes) > 0:
        hand_type = "Flush"
        hand = sorted(flushes[0],reverse=True)[0:5]
        return Hand(hand_type,hand)
    
    if len(straights) > 0:
        hand_type = "Straight"
        hand = straights[0]
        return Hand(hand_type,hand)
    
    if len(triples) > 0:
        hand_type = "Triples"
        hand = triples[0]
        if len(cards)-3 > 0:
            hand += individuals[0:min(2,len(cards)-3)]
        return Hand(hand_type,hand)  

    if len(pairs) >= 2:
        hand_type = "Double Pairs"
        hand = pairs[0] + pairs[1]
        if len(cards) > 4:
            hand.append(individuals[0])
        return Hand(hand_type,hand)
    
    if len(pairs) >= 1:
        hand_type = "Pairs"
        hand = pairs[0]
        if len(cards)-2 > 0:
            hand += individuals[0:min(3,len(cards)-2)]
        return Hand(hand_type,hand) 

    hand_type = 'High Card'
    if len(cards) > 5:
        hand = individuals[0:5]
    else:
        hand = individuals

    return Hand(hand_type,hand)

def get_flush_prob(cards: list[Card])-> float:
    prob = 0
    color_cuant = {i:0 for i in COLORS}
    remaining_cards = 52 - len(cards)
    cards_to_full = 7 - len(cards)
    for card in cards:
        color_cuant[card.color] += 1
    temp = 0
    for color in color_cuant:
        for i in range(cards_to_full-(5-color_cuant[color])+1):
            color_cards_needed = 5-color_cuant[color]+i
            temp += comb(13-color_cuant[color],color_cards_needed)*comb(remaining_cards-(13-color_cuant[color]),cards_to_full - color_cards_needed)
    prob = temp / comb(remaining_cards,cards_to_full)
    return prob

def get_royal_flush_prob(cards: list[Card])-> float:
    rflushes_nums = {color:5 for color in COLORS}
    cards_left = 7 - len(cards)
    for card in cards:
        if CARD_VALUES[card.value] >= 9:
            rflushes_nums[card.color] -= 1
    prob = 0
    for color in rflushes_nums:
        if rflushes_nums[color] > cards_left:
            continue
        prob += comb(52-(len(cards)-(5-rflushes_nums[color]))-rflushes_nums[color],cards_left-rflushes_nums[color])
    prob /= comb(52-len(cards),cards_left)
    return prob

def get_straight_flush_prob(cards: list[Card])-> float:
    cards_left = 7-len(cards)
    prob = 0
    for i in range(0,10):
        color_nums = {color:5 for color in COLORS}
        for card in cards:
            # Check cards left for the straight starting at i and with each color 
            # (if the card next to the straight is present it is imposible to do that straight so it is ignored)
            if  0 <= (CARD_VALUES[card.value]-i)%13 <= 4:
                color_nums[card.color] -= 1
            elif (CARD_VALUES[card.value]-i)%13 == 5:
                color_nums[card.color] = 1000
        for color in color_nums:
            if color_nums[color] > cards_left:
                continue
            # Same than royal streaight flush but with a -1 cause the next cards cant appear after
            if i==9:
                prob += comb(52-(len(cards)-(5-color_nums[color]))-color_nums[color],cards_left-color_nums[color])
            else:
                prob += comb(52-(len(cards)-(5-color_nums[color]))-color_nums[color]-1,cards_left-color_nums[color])
    prob /= comb(52-len(cards),cards_left)
    return prob

def get_poker_prob(cards: list[Card])-> float:
    cards_left = 7-len(cards)
    card_nums_left = {card:4 for card in CARD_VALUES}
    for card in cards:
        card_nums_left[card.value] -= 1
    prob = 0
    for card in card_nums_left:
        if card_nums_left[card] > cards_left:
            continue
        prob += comb(52-(len(cards)-(4-card_nums_left[card]))-card_nums_left[card],cards_left-card_nums_left[card])
    print(prob)
    prob /= comb(52-len(cards),cards_left)
    return prob

# TODO
def get_straight_prob(cards: list[Card])-> float:
    # This function doesnt take in to account straight hands that have a flush in them
    cards_left = 7-len(cards)
    prob = 0
    for i in range(0,10):
        cards_left_to_straight = 5
        appeared_straight_cards = set()
        cards_to_color = {c:5 for c in COLORS}
        for card in cards:
            # Check cards left for the straight starting at i and with each color 
            # (if the card next to the straight is present it is imposible to do that straight so it is ignored)
            cards_to_color[card.color] -= 1
            if  0 <= (CARD_VALUES[card.value]-i)%13 <= 4:
                cards_left_to_straight -= 1
                appeared_straight_cards.add(CARD_VALUES[card.value])
            elif (CARD_VALUES[card.value]-i)%13 == 5:
                cards_left_to_straight = 1000
        cards_left_to_choose = [k for k in range(i,i+5) if k not in appeared_straight_cards]
        if cards_left_to_straight > cards_left:
            continue
        repeated_cards_counted = {c:0 for c in COLORS}
        cards_counted = [set() for c in range(cards_left_to_straight)]
        for j in product(COLORS,repeat=cards_left_to_straight):
            available_cards1 = 52 - (len(cards) - (5-cards_left_to_straight)) - cards_left_to_straight
            available_cards2 = available_cards1
            new_cards_to_color = cards_to_color.copy()
            for color in j:
                new_cards_to_color[color] -= 1
            if any(new_cards_to_color[c] <= 0 for c in COLORS):
                continue
            for c in new_cards_to_color:
                if new_cards_to_color[c] == 1:
                    available_cards1 -= 13 - 4 
                    available_cards2 -= 13 - 4 
                elif new_cards_to_color[c] == 2:
                    available_cards2 -= 13 - 3 
            # TODO Change how repeated cards are counted taking into acount iut has to be reseted each time a color in j changes
            available_cards1 -= sum(len(k) for k in cards_counted) - len([1 for i,cl in enumerate(j) if cl in cards_counted[i]])
            available_cards2 -= sum(len(k) for k in cards_counted) - len([1 for i,cl in enumerate(j) if cl in cards_counted[i]])
            if cards_left-cards_left_to_straight == 0:
                prob += 1
            elif cards_left-cards_left_to_straight == 1:
                prob += available_cards1
            elif cards_left-cards_left_to_straight == 2:
                if j[0] == 'S':
                    print(j,available_cards1,available_cards2,new_cards_to_color)
                prob += comb(available_cards2,2)+(available_cards1-available_cards2)*available_cards2
            for k,color in enumerate(j):
                if color not in cards_counted[k]:
                    repeated_cards_counted[color] += 1
                    cards_counted[k].add(color)


    print(prob)
    prob /= comb(52-len(cards),cards_left)
    return prob

# h = get_best_hand([])
print(get_straight_flush_prob([])*100)
print(get_straight_prob([])*100)
