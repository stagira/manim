"""
Brief: Animation pédagogique RDMA over Ethernet via une SuperNIC (ManimCE)

Rôle du modèle
- Agir comme un expert en visualisation technique Manim (5+ ans d’expérience) pour sujets réseau/systèmes avancés.

Objectif
- Créer une animation claire et intuitive expliquant le fonctionnement de RDMA over Ethernet via une SuperNIC.

Détails de l’animation
1) Représentation d’une SuperNIC source (rectangle/icône).
2) Réseau de commutateurs (switchs) en cercles/carrés interconnectés (routes disponibles).
3) Paquets de données sous forme de boules/points lumineux se dispersant dans le réseau.
4) Paquets empruntant des routes différentes et arrivant correctement réassemblés à la destination (autre SuperNIC/serveur).
5) Annotation ou compteur illustrant le gain de bande passante effective (60% → 95%).
6) Flèches/effets lumineux illustrant le mouvement des paquets sur différents chemins.

Étapes à respecter dans le script
- Créer les objets statiques : SuperNIC source/destination, switchs, lignes de connexion.
- Générer les boules de données (points lumineux).
- Animer la dispersion dans le réseau avec effet lumineux.
- Montrer la réorganisation/réassemblage en sortie.
- Ajouter un indicateur visuel de performance (bande passante).

Contraintes
- Utiliser Manim Community Edition (ManimCE).
- Couleurs distinctes pour différencier paquets et chemins.
- Animation fluide, claire, pédagogique.
- Code commenté et structuré.

Format de sortie attendu
- Un fichier Python Manim complet contenant la classe de scène et les animations.
- Ce fichier implémente la scène `RDMAOverEthernet` (ci‑dessous).

Contenu de cette implémentation
- SuperNIC source/destination avec labels.
- Réseau de switchs et liens, offrant plusieurs chemins possibles.
- Paquets colorés se dispersant via plusieurs routes, avec effets lumineux.
- Visualisation du réassemblage : ligne d’arrivée désordonnée → ligne ordonnée.
- Indicateur de performance : barre + pourcentage animés de 60% à 95%.

Rendu / commandes utiles (ManimCE)
- Aperçu (qualité rapide) : `manim -pqh rdma_schema.py RDMAOverEthernet`
- Haute qualité MP4 : `manim -pqh --format=mp4 rdma_schema.py RDMAOverEthernet`
- Options pratiques : `-p` (ouvrir après rendu), `-q` (l,m,h), `-v WARNING` (logs réduits)

Notes
- Utilise les API ManimCE (Create, LaggedStart, MoveAlongPath, ShowPassingFlash, ValueTracker, always_redraw).
- Les couleurs distinguent paquets et chemins ; les durées varient pour simuler des arrivées désordonnées.
- Le réassemblage place d’abord les paquets dans une rangée d’arrivée arbitraire, puis les ordonne 1..N.
- La jauge de bande passante (60% → 95%) illustre le gain effectif.

Installation rapide ManimCE (environnement Python 3.9+ recommandé)
- 1) Créer un venv: `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)
- 2) Installer ManimCE: `pip install manim`
- 3) (Optionnel mais utile) FFMPEG pour export vidéo. Sur Windows/Mac, `pip install imageio-ffmpeg` suffit souvent.
- 4) Tester: `manim -v WARNING -qh --version`
- 5) Rendu de cette scène: `manim -pqh rdma_schema.py RDMAOverEthernet`

Exécution directe du script
- Vous pouvez lancer `python rdma_schema.py` pour rendre automatiquement la scène (aperçu activé) sans utiliser la CLI Manim.
"""

from manim import *
import numpy as np


class RDMAOverEthernet(Scene):
    """
    Animation pédagogique: RDMA over Ethernet via une SuperNIC.

    Étapes visuelles:
    1) Création d'un petit réseau (switchs + liens) entre deux SuperNICs.
    2) Génération de paquets (boules lumineuses) qui se dispersent dans le réseau par des chemins différents.
    3) Arrivée des paquets à la destination, puis réassemblage dans l'ordre.
    4) Indicateur de performance qui illustre le gain de bande passante (60% -> 95%).

    Conçu pour Manim Community Edition.
    """

    def construct(self):
        # ---------------------------------------------------------------
        # 1) Titre et mise en place de la scène
        # ---------------------------------------------------------------
        title = Text("RDMA over Ethernet via SuperNIC", weight=BOLD).scale(0.8)
        subtitle = Text("Chemins multiples, réassemblage fiable, bande passante accrue").scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.2)
        header = VGroup(title, subtitle).to_edge(UP, buff=0.5)

        self.play(FadeIn(header, shift=DOWN), run_time=0.8)

        # ---------------------------------------------------------------
        # 2) Objets statiques: SuperNIC source/destination, switchs, liens
        # ---------------------------------------------------------------
        # SuperNICs (source à gauche, destination à droite)
        nic_width, nic_height = 2.4, 1.0
        nic_src = RoundedRectangle(corner_radius=0.15, width=nic_width, height=nic_height, fill_opacity=0.05)
        nic_dst = RoundedRectangle(corner_radius=0.15, width=nic_width, height=nic_height, fill_opacity=0.05)
        nic_src.set_stroke(color=BLUE_C, width=2)
        nic_dst.set_stroke(color=GREEN_C, width=2)
        nic_src.to_edge(LEFT, buff=1.2)
        nic_dst.to_edge(RIGHT, buff=1.2)

        nic_src_lbl = Text("SuperNIC\nSource").scale(0.45)
        nic_dst_lbl = Text("SuperNIC\nDestination").scale(0.45)
        nic_src_lbl.move_to(nic_src.get_center())
        nic_dst_lbl.move_to(nic_dst.get_center())

        # Positions des switchs (petits carrés) entre source et destination
        # Placés pour former plusieurs chemins possibles.
        pos = {
            "s1": np.array([-2.2,  1.4, 0.0]),
            "s2": np.array([-2.2, -1.4, 0.0]),
            "s3": np.array([ 0.0,  2.1, 0.0]),
            "s4": np.array([ 0.0, -2.1, 0.0]),
            "s5": np.array([ 2.2,  1.4, 0.0]),
            "s6": np.array([ 2.2, -1.4, 0.0]),
        }

        def make_switch(name: str, p: np.ndarray, color=GREY_B):
            sw = Square(side_length=0.4)
            sw.set_stroke(color=GREY_B, width=2)
            sw.set_fill(color=GREY_E, opacity=0.2)
            sw.move_to(p)
            lbl = Text(name.upper()).scale(0.35).next_to(sw, DOWN, buff=0.1)
            return VGroup(sw, lbl)

        switches = {k: make_switch(k, p) for k, p in pos.items()}

        # Définition des liens (routes disponibles)
        # On force des segments simples qui couvrent plusieurs chemins.
        def L(a: np.ndarray, b: np.ndarray):
            line = Line(a, b)
            line.set_stroke(color=GREY_B, width=2)
            return line

        edges = [
            L(nic_src.get_right(), switches["s1"][0].get_left()),
            L(nic_src.get_right(), switches["s2"][0].get_left()),
            L(switches["s1"][0].get_right(), switches["s3"][0].get_left()),
            L(switches["s1"][0].get_right(), switches["s5"][0].get_left()),
            L(switches["s2"][0].get_right(), switches["s4"][0].get_left()),
            L(switches["s2"][0].get_right(), switches["s6"][0].get_left()),
            L(switches["s3"][0].get_right(), switches["s5"][0].get_left()),
            L(switches["s4"][0].get_right(), switches["s6"][0].get_left()),
            L(switches["s5"][0].get_right(), nic_dst.get_left()),
            L(switches["s6"][0].get_right(), nic_dst.get_left()),
        ]

        net_group = VGroup(nic_src, nic_dst, nic_src_lbl, nic_dst_lbl, *switches.values(), *edges)

        self.play(
            FadeIn(nic_src, shift=RIGHT), FadeIn(nic_dst, shift=LEFT),
            FadeIn(nic_src_lbl), FadeIn(nic_dst_lbl),
            LaggedStart(*[FadeIn(s, shift=DOWN*0.2) for s in switches.values()], lag_ratio=0.08),
            Create(VGroup(*edges), lag_ratio=0.1),
            run_time=2.2,
        )

        # ---------------------------------------------------------------
        # 3) Génération des paquets (boules lumineuses) et chemins
        # ---------------------------------------------------------------
        # Couleurs distinctes pour différencier paquets et chemins
        palette = [BLUE_C, GOLD_E, GREEN_C, PINK, PURPLE_B, TEAL_C]

        # Helper: construire un VMobject représentant un chemin en lignes brisées
        def build_path(points: list[np.ndarray]) -> VMobject:
            path = VMobject()
            path.set_points_as_corners(points)
            path.set_stroke(width=6, color=GREY_A, opacity=0.0)  # invisible; utilisé pour ShowPassingFlash
            return path

        # Points utilitaires
        src_pt = nic_src.get_right()
        dst_pt = nic_dst.get_left()
        s = {k: switches[k][0].get_center() for k in switches.keys()}

        # Définir quelques chemins multi-sauts plausibles
        path_A = build_path([src_pt, s["s1"], s["s3"], s["s5"], dst_pt])
        path_B = build_path([src_pt, s["s1"], s["s5"], dst_pt])
        path_C = build_path([src_pt, s["s2"], s["s4"], s["s6"], dst_pt])
        path_D = build_path([src_pt, s["s2"], s["s6"], dst_pt])

        paths = [path_A, path_D, path_B, path_C, path_A, path_D]  # 6 paquets -> 4 chemins réutilisés
        runtimes = [4.0, 2.6, 3.0, 3.5, 2.8, 4.2]  # Durées pour simuler arrivées désordonnées

        packets = []
        packet_anims = []
        flashes = []

        for i in range(6):
            color = palette[i % len(palette)]
            dot = Dot(point=src_pt, radius=0.065, color=color)
            dot.set_z_index(10)

            seq_lbl = Text(str(i + 1)).scale(0.35).next_to(dot, UP, buff=0.1)
            seq_lbl.set_color(color)
            pkt = VGroup(dot, seq_lbl)
            packets.append(pkt)

            # Animation de mouvement le long du chemin
            anim = MoveAlongPath(dot, paths[i], rate_func=linear, run_time=runtimes[i])
            # L’étiquette suit le dot
            seq_lbl.add_updater(lambda m, d=dot: m.next_to(d, UP, buff=0.1))
            packet_anims.append(anim)

            # Effet lumineux passant sur le chemin
            flash_trail = ShowPassingFlash(
                paths[i].copy().set_stroke(color=color, width=6, opacity=0.9),
                time_width=0.25,
                run_time=runtimes[i],
                rate_func=linear,
            )
            flashes.append(flash_trail)

        # Présenter les paquets au départ
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT*0.2) for p in packets], lag_ratio=0.1), run_time=1.2)

        # Disperser les paquets dans le réseau, avec effet lumineux sur les chemins
        self.play(
            AnimationGroup(
                LaggedStart(*flashes, lag_ratio=0.12),
                LaggedStart(*packet_anims, lag_ratio=0.12),
                lag_ratio=0.0,
            ),
            run_time=max(runtimes) + 0.1,
        )

        # ---------------------------------------------------------------
        # 4) Visualiser la réorganisation (réassemblage) à la destination
        # ---------------------------------------------------------------
        # Zone de buffer / rangements à côté de la destination
        buffer_title = Text("Buffer RDMA (réassemblage)").scale(0.45)
        buffer_title.next_to(nic_dst, UP, buff=0.5)

        # Deux rangées: ligne d'arrivée (désordonnée) et ligne réassemblée (1..N)
        slots_arrive = VGroup(*[Square(0.28).set_stroke(GREY_B, 1) for _ in range(6)])
        slots_order = VGroup(*[Square(0.28).set_stroke(GREY_B, 1) for _ in range(6)])
        slots_arrive.arrange(RIGHT, buff=0.12).next_to(nic_dst, RIGHT, buff=0.6).shift(UP*0.5)
        slots_order.arrange(RIGHT, buff=0.12).next_to(nic_dst, RIGHT, buff=0.6).shift(DOWN*0.5)

        lbl_arrive = Text("Arrivée (désordonnée)").scale(0.35).next_to(slots_arrive, UP, buff=0.15)
        lbl_order = Text("Réassemblage (1 → N)").scale(0.35).next_to(slots_order, DOWN, buff=0.15)

        self.play(FadeIn(buffer_title), FadeIn(slots_arrive), FadeIn(slots_order), FadeIn(lbl_arrive), FadeIn(lbl_order))

        # Définir un ordre d'arrivée arbitraire (désordonné) par index de paquet (1..6)
        arrival_order = [2, 5, 3, 6, 4, 1]

        # Placer les paquets dans l'ordre d'arrivée
        arrive_anims = []
        for idx, seq_num in enumerate(arrival_order):
            p = packets[seq_num - 1]  # paquet avec numéro seq_num
            arrive_anims.append(p.animate.move_to(slots_arrive[idx].get_center()))
        self.play(LaggedStart(*arrive_anims, lag_ratio=0.12), run_time=2.0)

        # Mettre en évidence le besoin de réassemblage
        brace = BraceBetweenPoints(slots_arrive.get_left() + DOWN*0.25, slots_order.get_left() + UP*0.25, color=YELLOW)
        brace_txt = Text("Réassemblage par la SuperNIC").scale(0.35).next_to(brace, LEFT, buff=0.1)
        self.play(GrowFromCenter(brace), FadeIn(brace_txt))

        # Réordonner les paquets: les mettre dans l'ordre 1..6
        reorder_anims = []
        for i in range(6):
            target_slot = slots_order[i].get_center()
            pkt = packets[i]  # i == seq_num-1 -> ordre correct 1..6
            reorder_anims.append(pkt.animate.move_to(target_slot))
        self.play(LaggedStart(*reorder_anims, lag_ratio=0.1), run_time=2.0)

        # Petit highlight pour valider l'ordre
        ok_rect = SurroundingRectangle(slots_order, color=GREEN_C, buff=0.12)
        self.play(Create(ok_rect), run_time=0.6)
        self.play(ok_rect.animate.set_stroke(opacity=0.0), run_time=0.6)

        # ---------------------------------------------------------------
        # 5) Indicateur visuel de performance (bande passante 60% -> 95%)
        # ---------------------------------------------------------------
        meter_title = Text("Bande passante effective").scale(0.45)
        meter_title.to_corner(UL).shift(DOWN*0.2 + RIGHT*0.3)

        bar_bg = Rectangle(width=4.0, height=0.28, stroke_color=GREY_B, stroke_width=1)
        bar_bg.set_fill(GREY_E, opacity=0.4)
        bar_bg.next_to(meter_title, DOWN, buff=0.2).to_edge(LEFT, buff=0.6)

        percent = ValueTracker(60)

        def make_bar():
            w = bar_bg.width * (percent.get_value() / 100.0)
            w = max(0.02, min(bar_bg.width, w))
            bar = Rectangle(width=w, height=bar_bg.height - 0.06)
            bar.set_fill(GREEN_C, opacity=0.9)
            bar.set_stroke(width=0)
            bar.move_to(LEFT*(bar_bg.width/2 - w/2))
            bar.align_to(bar_bg, LEFT)
            bar.move_to([bar_bg.get_left()[0] + w/2, bar_bg.get_center()[1], 0.0])
            return bar

        bar_fg = always_redraw(make_bar)

        percent_text = always_redraw(
            lambda: Text(f"{percent.get_value():.0f}%").scale(0.45).next_to(bar_bg, RIGHT, buff=0.2)
        )

        self.play(FadeIn(meter_title), FadeIn(bar_bg))
        self.add(bar_fg, percent_text)

        # Animation: 60% -> 95%
        self.play(percent.animate.set_value(95), run_time=2.0, rate_func=smooth)

        # Quelques touches finales
        gain_txt = Text("Gain: +35 points").scale(0.4).next_to(percent_text, DOWN, buff=0.1)
        self.play(FadeIn(gain_txt, shift=UP), run_time=0.6)

        # Pause pour apprécier l'ensemble
        self.wait(1.0)

        # Fin: léger zoom-out pour récap visuel
        self.play(
            self.camera.frame.animate.scale(1.06).move_to(net_group.get_center()),
            run_time=1.0,
        )
        self.wait(0.6)

if __name__ == "__main__":
    # Exécution directe: rend la scène avec prévisualisation et qualité moyenne
    from manim import tempconfig

    with tempconfig({"quality": "medium_quality", "preview": True}):
        RDMAOverEthernet().render()
