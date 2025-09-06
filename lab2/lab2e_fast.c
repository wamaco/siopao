#include "panopticon.h"
#include <stdlib.h>
#include <stdint.h>

typedef struct node {
    int64_t floor;
    const char *guest;
    int64_t pri;
    struct node *left;
    struct node *right;
} node;

struct tower_spy {
    node *g_flrs;
    int64_t n_g;
};

static node *new_node(const char *g, int64_t f) {
    node *nd = (node *)malloc(sizeof(node));
    if (!nd) {
        return NULL;
    }
    nd->floor = f;
    nd->guest = g;
    nd->pri = oj_rand();
    nd->left = nd->right = NULL;
    return nd;
}

static node *rotate_right(node *y) {
    node *x = y->left;
    y->left = x->right;
    x->right = y;
    return x;
}

static node *rotate_left(node *x) {
    node *y = x->right;
    x->right = y->left;
    y->left = x;
    return y;
}

static node *treap_insert(node *root, const char *g, int64_t f) {
    if (!root) {
        return new_node(g, f);
    }

    if (f < root->floor) {
        root->left = treap_insert(root->left, g, f);
        if (root->left && root->left->pri < root->pri) {
            root = rotate_right(root);
        }
    } else {
        root->right = treap_insert(root->right, g, f);
        if (root->right && root->right->pri < root->pri) {
            root = rotate_left(root);
        }
    }
    return root;
}

static node *find_node(node *root, int64_t f) {
    while (root) {
        if (f == root->floor) {
            return root;
        } else if (f < root->floor) {
            root = root->left;
        } else {
            root = root->right;
        }
    }
    return NULL;
}

static node *predecessor_value(node *root, int64_t f) {
    node *res = NULL;
    while (root) {
        if (root->floor < f) {
            res = root;
            root = root->right;
        } else {
            root = root->left;
        }
    }
    return res;
}

static node *successor_value(node *root, int64_t f) {
    node *res = NULL;
    while (root) {
        if (root->floor > f) {
            res = root;
            root = root->left;
        } else {
            root = root->right;
        }
    }
    return res;
}

tower_spy *t_init(int64_t n) {
    (void)n;
    tower_spy *t = (tower_spy *)malloc(sizeof(*t));
    if (!t) {
        return NULL;
    }
    t->g_flrs = NULL;
    t->n_g = 0;
    return t;
}

void purchase(tower_spy *t, const char *g, int64_t f) {
    t->g_flrs = treap_insert(t->g_flrs, g, f);
    t->n_g++;
}

static int better_than(node *a, node *b, int64_t f) {
    if (!a) {
        return 0;
    }
    if (!b) {
        return 1;
    }
    int64_t da = a->floor - f;
    if (da < 0) {
        da = -da;
    }
    int64_t db = b->floor - f;
    if (db < 0) {
        db = -db;
    }
    if (da < db) {
        return 1;
    }
    if (da > db) {
        return 0;
    }
    return a->floor < b->floor;
}

two_names two_nearest(tower_spy *t, int64_t f) {
    two_names res;
    res.nearest = NULL;
    res.snd_nearest = NULL;

    if (t->n_g <= 2) {
        return res;
    }

    node *cur = find_node(t->g_flrs, f);
    if (!cur) {
        node *left = predecessor_value(t->g_flrs, f);
        node *right = successor_value(t->g_flrs, f);
        node *cand[4];
        int cnt = 0;
        if (left) {
            cand[cnt++] = left;
        }
        if (left) {
            node *l2 = predecessor_value(t->g_flrs, left->floor);
            if (l2) {
                cand[cnt++] = l2;
            }
        }
        if (right) {
            cand[cnt++] = right;
        }
        if (right) {
            node *r2 = successor_value(t->g_flrs, right->floor);
            if (r2) {
                cand[cnt++] = r2;
            }
        }
        if (cnt < 2) {
            return res;
        }
        int best = -1, snd = -1;
        int s;
        for (s = 0; s < cnt; s++) {
            if (best == -1 || better_than(cand[s], cand[best], f)) {
                best = s;
            }
        }
        for (s = 0; s < cnt; s++) {
            if (s == best) {
                continue;
            }
            if (snd == -1 || better_than(cand[s], cand[snd], f)) {
                snd = s;
            }
        }
        if (best != -1 && snd != -1) {
            res.nearest = cand[best]->guest;
            res.snd_nearest = cand[snd]->guest;
        }
        return res;
    }

    node *left1 = predecessor_value(t->g_flrs, f);
    node *left2 = NULL;
    if (left1) {
        left2 = predecessor_value(t->g_flrs, left1->floor);
    }
    node *right1 = successor_value(t->g_flrs, f);
    node *right2 = NULL;
    if (right1) {
        right2 = successor_value(t->g_flrs, right1->floor);
    }

    node *cand[4];
    int cnt = 0;
    if (left1) {cand[cnt++] = left1;}
    if (left2) {cand[cnt++] = left2;}
    if (right1) {cand[cnt++] = right1;}
    if (right2) {cand[cnt++] = right2;}

    if (cnt < 2) {return res;}

    int best = -1, snd = -1;
    int s;
    for (s = 0; s < cnt; s++) {
        if (best == -1 || better_than(cand[s], cand[best], f)) {best = s;}
    }
    for (s = 0; s < cnt; s++) {
        if (s == best) {continue;}
        if (snd == -1 || better_than(cand[s], cand[snd], f)) {snd = s;}
    }

    if (best != -1 && snd != -1) {
        res.nearest = cand[best]->guest;
        res.snd_nearest = cand[snd]->guest;
    }
    return res;
}
