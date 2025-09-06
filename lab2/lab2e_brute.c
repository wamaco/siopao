#include "panopticon.h"
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <limits.h>

typedef struct {
    const char *guest;
    int64_t floor;
} g_flr_entry;

struct tower_spy {
    g_flr_entry *g_flrs; // username
    int64_t n_g;         // username for guest num
    int64_t capacity;
};

tower_spy *t_init(int64_t n) {
    tower_spy *t = (tower_spy *)malloc(sizeof(*t));
    if (!t) {
        return NULL;
    }
    t->capacity = 16;
    t->n_g = 0;
    t->g_flrs = (g_flr_entry *)malloc(sizeof(g_flr_entry) * t->capacity);
    if (!t->g_flrs) {
        free(t);
        return NULL;
    }
    return t;
}

void purchase(tower_spy *t, const char *g, int64_t f) {
    if (t->n_g == t->capacity) {
        t->capacity *= 2;
        g_flr_entry *tmp = (g_flr_entry *)realloc(t->g_flrs, sizeof(g_flr_entry) * t->capacity);
        if (tmp) {
            t->g_flrs = tmp;
        } else {
            // the alloc failed :(
            t->capacity /= 2;
            return;
        }
    }
    t->g_flrs[t->n_g].guest = g;
    t->g_flrs[t->n_g].floor = f;
    t->n_g++;
}

two_names two_nearest(tower_spy *t, int64_t f) {
    two_names res;
    res.nearest = NULL;
    res.snd_nearest = NULL;

    // if fewer than two guests, ret null null
    if (t->n_g <= 2) {
        return res;
    }

    int64_t s;
    int64_t best_dist = INT64_MAX;
    int64_t snd_best_dist = INT64_MAX;
    int64_t best_idx = -1;
    int64_t snd_idx = -1;
    int64_t dist;
    int64_t candidate_floor;
    int64_t best_floor;
    int64_t snd_floor;

    for (s = 0; s < t->n_g; s++) {
        if (t->g_flrs[s].floor == f) {
            continue;
        }

        candidate_floor = t->g_flrs[s].floor;
        dist = candidate_floor - f;
        if (dist < 0) {
            dist = -dist;
        }

        if (best_idx == -1) {
            best_dist = dist;
            best_idx = s;
            continue;
        }

        best_floor = t->g_flrs[best_idx].floor;

        if (dist < best_dist || (dist == best_dist && candidate_floor < best_floor)) {
            snd_best_dist = best_dist;
            snd_idx = best_idx;

            best_dist = dist;
            best_idx = s;
        } else {
            if (snd_idx == -1) {
                snd_best_dist = dist;
                snd_idx = s;
            } else {
                snd_floor = t->g_flrs[snd_idx].floor;
                if (dist < snd_best_dist || (dist == snd_best_dist && candidate_floor < snd_floor)) {
                    snd_best_dist = dist;
                    snd_idx = s;
                }
            }
        }
    }

    if (best_idx != -1 && snd_idx != -1) {
        res.nearest = t->g_flrs[best_idx].guest;
        res.snd_nearest = t->g_flrs[snd_idx].guest;
    } else {
        res.nearest = NULL;
        res.snd_nearest = NULL;
    }
    return res;
}
