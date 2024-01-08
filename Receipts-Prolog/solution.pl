% Informace o projektu:
% Zkratka fakulty: FIT ČVUT
% Zkratka předmětu: BI-ZNS
% Akademický rok: ZS2023
% Jméno studenta: Dmytro Borovko
% Úkol: Tento projekt je řešením 1. úlohy, která zahrnuje vytvoření znalostního systému v Prologupro ověřování faktur a účtenek podle určených kritérií. 
% Systém poskytuje konzultace nekvalifikovaným uživatelům pro hodnocení správnosti údajů v dokumentech.

% Hlavní tělo programu zodpovídá za vypsání úvodního textu, který uživatele zavádí do problematiky, provedení dotazu a výpis výsledků.

:- initialization(start).

start :- writeln('Pro zahájení komunikace s expertním systémem napište "main.".'), read(X), X = main, main.

main :- identifikace.

identifikace:-
    retractall(known(_,_)),
    writeln('Vítá vás jednoduchý expertní systém, který poskytuje konzultace uživatelům při posuzování správnosti údajů na účtence.'),
    writeln('Prosím odpovídejte na dotazy ano nebo ne. Jinak vám nemohu pomoci. Každou odpověď je třeba zakončit tečkou.'), nl,
    chyba(X), nl,
    write('Byla zjištěna chyba v účtence: '), write(X), nl, !.

identifikace:- 
    nl, writeln('Vypadá to tak, že tento doklad neobsahuje žádné z těch třinácti chyb, o kterých mám znalost. Nicméně nemůžu s jistotou potvrdit, že neexistuje jiná neznámá chyba.').

% --------------------------------
% Báze znalostí
% --------------------------------

chyba('Chybí údaje o dodavateli (IČO).') :- 
    ma_ico_dodavatele(ne).

chyba('Neplatné IČO dodavatele.') :- 
    ma_ico_dodavatele(ano),
    spravne_ico_dodavatele(ne).

chyba('Neplatné DIČ dodavatele.') :- 
    je_danovy_doklad(ano),
    spravne_dic_dodavatele(ne).

chyba('Neplatné IČO odběratele.') :- 
    ma_ico_odberatele(ano),
    spravne_ico_odberatele(ne).

chyba('Neplatné DIČ odběratele.') :- 
    je_danovy_doklad(ano),
    ma_nazev_odberatele(ano),
    spravne_dic_odberatele(ne).

chyba('Chybná celková částka.') :- 
    shodnost_souctu(ne).

chyba('Chybí datum uskutečnění zdanitelného plnění.') :- 
    ma_datum(ne).

chyba('Chyba v datu.') :- 
    ma_datum(ano),
    spravne_datum(ne).

chyba('Chybí rekapitulace DPH.') :- 
    je_danovy_doklad(ano),
    ma_rekapitulaci_dph(ne),
    ma_sazbu_dph(ne).

chyba('Chybné sazby DPH.') :- 
    jsou_potraviny_uctovane(ano),
    jedna_se_o_deset_procent(ano),
    jsou_potraviny_tady_konzumovane(ne).

chyba('Chybí údaje o zápisu dodavatele do živnostenského nebo obchodního rejstříku.') :-
    je_v_obchodnim_rejstriku(ne),
    je_v_zivnostenskem_rejstriku(ne).

chyba('Chybí číslo dokladu.') :- 
    ma_cislo_dokladu(ne).

chyba('Jedná se o zjednodušený daňový doklad, ale celková částka je přes 10.000 Kč.') :- 
    je_danovy_doklad(ano),
    ma_nazev_odberatele(ne),
    castka_pres_deset_tisic(ano).

% --------------------------------
% Uživatelské rozhraní
% --------------------------------
ma_ico_odberatele(X) :- dotaz('Je na dokladu uvedeno IČO odběratele?', ma_ico_odberatele, X).
je_danovy_doklad(X) :- dotaz('Je na dokladu uvedeno DIČ dodavatele?', je_danovy_doklad, X).
ma_nazev_odberatele(X) :- dotaz('Je na dokladu uveden název odběratele?', ma_nazev_odberatele, X).
ma_ico_dodavatele(X) :- dotaz('Je na dokladu uvedeno IČO dodavatele?', ma_ico_dodavatele, X).
shodnost_souctu(X) :- dotaz('Spočítejte prosím ručně celkový součet položek na dokladu. Shoduje se ten součet s celkovým součtem uvedeným na dokladu?', shodnost_souctu, X).
ma_rekapitulaci_dph(X) :- dotaz('Je na dokladu obsažena rekapitulace DPH?', ma_rekapitulaci_dph, X).
ma_sazbu_dph(X) :- dotaz('Je na dokladu uvedena sazba DPH pro celkovou částku?', ma_sazbu_dph, X).
ma_datum(X) :- dotaz('Je na dokladu uvedeno datum vystavení?', ma_datum, X).
spravne_datum(X) :- dotaz('Je datum na dokladu platné a odpovídá roku 2021?', spravne_datum, X).
jsou_potraviny_uctovane(X) :- dotaz('Jsou na dokladu účtovány potraviny?', jsou_potraviny_uctovane, X).
jedna_se_o_deset_procent(X) :- dotaz('Jedná se o sazbu DPH 10%?', jedna_se_o_deset_procent, X).
jsou_potraviny_tady_konzumovane(X) :- dotaz('Jsou položky v sazbě DPH 10% konzumovány v prostorách dodavatele?', jsou_potraviny_tady_konzumovane, X).
je_v_obchodnim_rejstriku(X) :- dotaz('Jsou na účtence obsaženy údaje o zápisu dodavatele do obchodního rejstříku?', je_v_obchodnim_rejstriku, X).
je_v_zivnostenskem_rejstriku(X) :- dotaz('Jsou na účtence uvedeny údaje o zápisu dodavatele do živnostenského rejstříku?', je_v_zivnostenskem_rejstriku, X).
ma_cislo_dokladu(X) :- dotaz('Je na dokladu obsaženo číslo dokladu?', ma_cislo_dokladu, X).
castka_pres_deset_tisic(X) :- dotaz('Je celková částka větší než 10.000 Kč?', castka_pres_deset_tisic, X).

spravne_ico_dodavatele(X) :- spravne_ico(spravne_ico_dodavatele, X).
spravne_ico_odberatele(X) :- spravne_ico(spravne_ico_odberatele, X).
spravne_dic_dodavatele(X) :- spravne_dic(spravne_dic_dodavatele, X).
spravne_dic_odberatele(X) :- spravne_dic(spravne_dic_odberatele, X).

spravne_ico(Y, X) :- kontrola_ico(Y, Kn), Kn = X.
spravne_dic(Y, X) :- kontrola_dic(Y, Kn), Kn = X.

% --------------------------------
% Implementace kontroly IČO a DIČ
% --------------------------------

kontrola_ico(Y, X) :- je_zname(Y, X), !.
kontrola_ico(Y, X) :- precti_ico(Y), known(Y, X).

kontrola_dic(Y, X) :- je_zname(Y, X), !.
kontrola_dic(Y, X) :- precti_dic(Y), known(Y, X).

je_zname(Y, X) :- known(Y, ano), X = ano, !.
je_zname(Y, X) :- known(Y, ne), X = ne.

precti_ico(Y) :-
    write('Zadejte IČO (bez tečky na konci): '),
    read_line_to_codes(user_input, _), % to read '\n' that remained in input buffer
    read_line_to_codes(user_input, Codes),
    atom_codes(String, Codes),
    atom_number(String, Number),
    validace_ico(String, Number, Y),
    vypocitej(Number, Y).    

validace_ico(String, Number, _) :-
    integer(Number),
    string_chars(String, CharList),
    pocet_cislic(CharList, Count),
    Count = 8, !.

validace_ico(String, _, Y) :-
    write('IČO '), write(String), write(' je neplatné. Číslo musí být osmimístné. Chcete uvést IČO znovu? (ano nebo ne): '), nl,
    read(A),
    A = ano,
    precti_ico(Y), !.

validace_ico(_, _, Y) :-
    asserta(known(Y, ne)).

precti_dic(Y) :-
    write('Zadejte DIČ (bez tečky na konci): '),
    read_line_to_codes(user_input, _), % to read '\n' that remained in input buffer
    read_line_to_codes(user_input, Codes),
    odstran_prefix(Codes, Dic, 2),
    atom_codes(String, Dic),
    atom_number(String, Number),
    validace_dic(String, Number, Y),
    vypocitej(Number, Y).    

validace_dic(String, Number, _) :-
    integer(Number),
    string_chars(String, CharList),
    pocet_cislic(CharList, Count),
    Count = 8, !.

validace_dic(String, _, Y) :-
    write('Číslo po kódu státu v DIČ '), write(String), write(' je neplatné. Číslo musí být osmimístné. Chcete uvést DIČ znovu? (ano nebo ne): '), nl,
    read(A),
    A = ano,
    precti_dic(Y), !.

validace_dic(_, _, Y) :-
    asserta(known(Y, ne)).

odstran_prefix(Input, Output, 0) :- Input = Output, !.

odstran_prefix([_|Rest], Output, N) :-
    N > 0,
    NewN is N - 1,
    odstran_prefix(Rest, Output, NewN).

int_to_list(0, []) :- !.
int_to_list(N, [Digit | Rest]) :-
    Digit is N mod 10,
    Next is N // 10,
    int_to_list(Next, Rest).

pocet_cislic([], 0).

pocet_cislic([_ | Tail], Count) :-
    pocet_cislic(Tail, TailCount),
    Count is TailCount + 1.

vypocitej(_, Y) :- known(Y, ano), !.

vypocitej(_, Y) :- known(Y, ne), !.

vypocitej(Number, Y) :-
    int_to_list(Number, Reversed_List),
    reverse_list(Reversed_List, List),
    vypocitej_soucet(List, [8, 7, 6, 5, 4, 3, 2, 0], Sum),
    Zbytek is Sum mod 11,
    vypocitej_c_ze_zbytku(Zbytek, C),
    last_digit(Reversed_List, Last),
    porovnej_c(Last, C, Y).

reverse_list([], []).
reverse_list([X|Xs], Reversed) :- reverse_list(Xs, Rest), append(Rest, [X], Reversed).

vypocitej_soucet([], [], 0).
vypocitej_soucet([Digit | Rest], [Digit_mult | Rest_mult], Sum) :-
    vypocitej_soucet(Rest, Rest_mult, RestSum),
    Sum is RestSum + Digit * Digit_mult.

vypocitej_c_ze_zbytku(0, 1) :- !.
vypocitej_c_ze_zbytku(10, 1) :- !.
vypocitej_c_ze_zbytku(1, 0) :- !.
vypocitej_c_ze_zbytku(Zbytek, C) :- C is 11 - Zbytek.

last_digit([Last | _], Last).

porovnej_c(Last, C, Y) :- Last = C, asserta(known(Y, ano)), !.
porovnej_c(Last, C, Y) :- Last \= C, asserta(known(Y, ne)).

% --------------------------------
% Implementace klauzuli dotaz
% --------------------------------

dotaz(_,X,A):-
    known(X, Kn), A = Kn, !.       
                           
dotaz(_,X,A):-
    known(X, Kn), A \= Kn, !, fail.

dotaz(Q,X,A):-
    write(Q), write(' (ano nebo ne): '),
    read(Kn),                          
    asserta(known(X,Kn)),
    A = Kn.      

