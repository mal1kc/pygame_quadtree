from __future__ import annotations
import enum
import pygame


class QuadtreePlacement(enum.Enum):
    TOPLEFT = enum.auto()
    TOPRIGHT = enum.auto()
    BOTTOMLEFT = enum.auto()
    BOTTOMRIGHT = enum.auto()


# a mapping data to make easy to creation
class QuadtreeFlag:
    childs: tuple[
        QuadtreeFlag | None,
        QuadtreeFlag | None,
        QuadtreeFlag | None,
        QuadtreeFlag | None,
    ]

    def __init__(
        self,
        childs: tuple[
            QuadtreeFlag | None,
            QuadtreeFlag | None,
            QuadtreeFlag | None,
            QuadtreeFlag | None,
        ],
    ):
        self.childs = childs

    def __iter__(self):
        for ch in self.childs:
            yield ch


def get_example_quadtreeflag() -> QuadtreeFlag:
    example_tree_flag = QuadtreeFlag(
        childs=(
            QuadtreeFlag(
                (
                    QuadtreeFlag(
                        (None, None, None, QuadtreeFlag((None, None, None, None)))
                    ),
                    None,
                    QuadtreeFlag(
                        (
                            None,
                            None,
                            None,
                            QuadtreeFlag(
                                (
                                    None,
                                    None,
                                    None,
                                    QuadtreeFlag((None, None, None, None)),
                                )
                            ),
                        )
                    ),
                    None,
                )
            ),
            QuadtreeFlag(
                (
                    None,
                    None,
                    QuadtreeFlag(
                        (None, None, None, QuadtreeFlag((None, None, None, None)))
                    ),
                    QuadtreeFlag(
                        (
                            QuadtreeFlag(
                                (
                                    None,
                                    QuadtreeFlag((None, None, None, None)),
                                    QuadtreeFlag((None, None, None, None)),
                                    QuadtreeFlag((None, None, None, None)),
                                )
                            ),
                            QuadtreeFlag((None, None, None, None)),
                            QuadtreeFlag((None, None, None, None)),
                            None,
                        )
                    ),
                )
            ),
            QuadtreeFlag((None, None, None, None)),
            QuadtreeFlag(
                (
                    QuadtreeFlag(
                        (None, QuadtreeFlag((None, None, None, None)), None, None)
                    ),
                    None,
                    QuadtreeFlag(
                        (None, None, None, QuadtreeFlag((None, None, None, None)))
                    ),
                    None,
                )
            ),
        )
    )
    return example_tree_flag


def append_childs_recursive_quad(root: Quadtree, quadTreeFlag: QuadtreeFlag):
    for indx, ch_flag in enumerate(quadTreeFlag):
        if isinstance(ch_flag, QuadtreeFlag):
            placement = QuadtreePlacement(indx + 1)
            quad_child = root.add_child(placement)
            if quad_child:
                append_childs_recursive_quad(quad_child, ch_flag)


def create_quadtree_from_QuadtreeFlag(
    surface: pygame.Surface, quadTreeFlag: QuadtreeFlag, position: pygame.Vector2
):
    _ = quadTreeFlag
    _ = surface
    root = Quadtree(surface, position)
    append_childs_recursive_quad(root, quadTreeFlag)
    print(root)
    return root


# equaly splitting Quadtree
class Quadtree:
    __slots__ = (
        "parent",
        "childs",
        "area",
        "position",
        "placement",
        "size",
        "font",
        "depth",
    )

    def __init__(
        self,
        parent_or_area: Quadtree | pygame.Surface,
        position: pygame.Vector2 | None = None,
    ):
        if isinstance(parent_or_area, Quadtree):
            self.parent = parent_or_area
            self.area = None
        else:
            self.area = parent_or_area
            self.parent = None
        self.childs: list[Quadtree] = []
        self.placement: QuadtreePlacement = QuadtreePlacement.TOPLEFT
        self.position = position if position else pygame.Vector2(0, 0)
        self.depth = 0
        if self.area:
            size = self.area.get_size()
            self.size = pygame.Vector2(size[0], size[1])
        if self.parent:
            self.size = self.parent.size / 2

        self.font = pygame.font.SysFont("Iosevka", 10)

    def add_child(
        self, placement: QuadtreePlacement = QuadtreePlacement.TOPLEFT
    ) -> Quadtree | None:
        new_ch = Quadtree(parent_or_area=self)
        new_ch.placement = placement
        if len(self.childs) >= 4:
            raise UserWarning("maximum child count is 4 because it is Quadtree")
        if not any(
            (oth_child.placement == new_ch.placement for oth_child in self.childs)
        ):
            match new_ch.placement:
                case QuadtreePlacement.TOPLEFT:
                    new_ch.position = self.position
                case QuadtreePlacement.TOPRIGHT:
                    new_ch.position = pygame.Vector2(
                        self.position.x + self.size.x / 2, self.position.y
                    )
                case QuadtreePlacement.BOTTOMLEFT:
                    new_ch.position = pygame.Vector2(
                        self.position.x, self.position.y + self.size.y / 2
                    )
                case QuadtreePlacement.BOTTOMRIGHT:
                    new_ch.position = pygame.Vector2(
                        self.position.x + self.size.x / 2,
                        self.position.y + self.size.y / 2,
                    )
            new_ch.depth = self.depth + 1
            self.childs.append(new_ch)
            return new_ch

    # def __repr__(self):
    #     return (
    #         " " * self.depth
    #         + "-"
    #         + "\n"
    #         + "".join((ch.__repr__() if ch else "" for ch in self.childs) # : ignore[reportUnknownArgumentType]
    #     )

    def draw(
        self,
        color: pygame.Color,
        surface: pygame.Surface,
    ):
        if len(self.childs) == 0:
            rect = pygame.Rect(
                self.position.x, self.position.y, self.size.x, self.size.y
            )
            if rect:
                _ = pygame.draw.rect(surface, color, rect)
                placement_text = f"{self.placement.name}"
                text_surface = self.font.render(placement_text, True, (0, 0, 0))
                text_rect = text_surface.get_rect(
                    center=rect.center
                )  # Center the text in the rect
                _ = surface.blit(text_surface, text_rect)
        else:
            # draw a thin white seperator lines
            vert_line_pos = (
                pygame.Vector2(self.position.x + self.size.x / 2, self.position.y),
                pygame.Vector2(
                    self.position.x + self.size.x / 2, self.position.y + self.size.y
                ),
            )

            horiz_line_pos = (
                pygame.Vector2(self.position.x, self.position.y + self.size.y / 2),
                pygame.Vector2(
                    self.position.x + self.size.x, self.position.y + self.size.y / 2
                ),
            )

            _ = pygame.draw.line(surface, color, vert_line_pos[0], vert_line_pos[1])
            _ = pygame.draw.line(surface, color, horiz_line_pos[0], horiz_line_pos[1])

        for ch in self.childs:
            ch.draw(
                color,
                surface,
            )
