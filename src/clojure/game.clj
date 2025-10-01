
#!/usr/bin/env bb

(ns game
  (:require [clojure.string :as str]))

(declare check-win)

(defn create-cell
  []
  {:has-mine false
   :is-revealed false
   :is-flagged false
   :adjacent-mines 0})

(defn create-empty-board
  [width height]
  (vec (repeat height (vec (repeat width (create-cell))))))

(defn get-neighbors
  [row col height width]
  (for [dr [-1 0 1]
        dc [-1 0 1]
        :when (not (and (= dr 0) (= dc 0)))
        :let [nr (+ row dr)
              nc (+ col dc)]
        :when (and (>= nr 0) (< nr height)
                   (>= nc 0) (< nc width))]
    [nr nc]))

(defn place-mines
  [board mines-count first-click]
  (let [height (count board)
        width (count (first board))
        available (for [r (range height)
                       c (range width)]
                   [r c])
        forbidden (if first-click
                   (let [[fr fc] first-click]
                     (conj (set (get-neighbors fr fc height width)) first-click))
                   #{})
        positions (remove forbidden available)
        mine-positions (set (take mines-count (shuffle positions)))]
    (vec (for [r (range height)]
           (vec (for [c (range width)]
                  (if (contains? mine-positions [r c])
                    (assoc (get-in board [r c]) :has-mine true)
                    (get-in board [r c]))))))))

(defn calculate-adjacent-mines
  [board]
  (let [height (count board)
        width (count (first board))]
    (vec (for [r (range height)]
           (vec (for [c (range width)]
                  (let [cell (get-in board [r c])]
                    (if (:has-mine cell)
                      cell
                      (let [neighbors (get-neighbors r c height width)
                            mine-count (count (filter #(get-in board (conj % :has-mine))
                                                     neighbors))]
                        (assoc cell :adjacent-mines mine-count))))))))))

(defn init-game
  [width height mines-count]
  {:width width
   :height height
   :board (create-empty-board width height)
   :game-over false
   :won false
   :mines-count mines-count})

(defn is-first-move?
  [state]
  (not-any? #(:is-revealed %)
            (apply concat (:board state))))

(defn reveal-cell
  [state row col]
  (let [{:keys [board width height game-over mines-count]} state]
    (cond
      game-over state
      (or (< row 0) (>= row height) (< col 0) (>= col width)) state
      :else
      (let [cell (get-in board [row col])]
        (cond
          (:is-revealed cell) state
          (:is-flagged cell) state
          :else
          (let [board (if (is-first-move? state)
                       (-> board
                           (place-mines mines-count [row col])
                           calculate-adjacent-mines)
                       board)
                cell (get-in board [row col])
                new-board (assoc-in board [row col :is-revealed] true)]
            (cond
              (:has-mine cell)
              (let [revealed-board
                    (vec (for [r (range height)]
                           (vec (for [c (range width)]
                                  (let [cell (get-in new-board [r c])]
                                    (if (:has-mine cell)
                                      (assoc cell :is-revealed true)
                                      cell))))))]
                (assoc state
                       :board revealed-board
                       :game-over true
                       :won false))
              (= 0 (:adjacent-mines cell))
              (let [temp-state (assoc state :board new-board)
                    neighbors (get-neighbors row col height width)]
                (reduce (fn [st [nr nc]]
                          (reveal-cell st nr nc))
                        temp-state
                        neighbors))
              :else
              (let [new-state (assoc state :board new-board)]
                (check-win new-state)))))))))

(defn toggle-flag
  [state row col]
  (let [{:keys [board width height game-over]} state]
    (cond
      game-over state
      (or (< row 0) (>= row height) (< col 0) (>= col width)) state
      :else
      (let [cell (get-in board [row col])]
        (if (:is-revealed cell)
          state
          (let [new-board (update-in board [row col :is-flagged] not)
                new-state (assoc state :board new-board)]
            (check-win new-state)))))))

(defn check-win
  [state]
  (if (:game-over state)
    state
    (let [unrevealed-safe (count (filter #(and (not (:has-mine %))
                                               (not (:is-revealed %)))
                                         (apply concat (:board state))))]
      (if (= unrevealed-safe 0)
        (assoc state :game-over true :won true)
        state))))

(defn count-flags
  [state]
  (count (filter :is-flagged (apply concat (:board state)))))

(defn clear-screen []
  (print "\033[2J\033[H")
  (flush))

(defn print-board [state]
  (let [{:keys [board width height]} state]
    (println)
    (print "  ")
    (doseq [c (range width)]
      (print (format " %d" c)))
    (println)
    (doseq [r (range height)]
      (print (format "%2d" r))
      (doseq [c (range width)]
        (let [cell (get-in board [r c])]
          (cond
            (:is-flagged cell) (print " 🚩")
            (not (:is-revealed cell)) (print " ▢")
            (:has-mine cell) (print " 💣")
            (= 0 (:adjacent-mines cell)) (print "  ")
            :else (print (format " %d" (:adjacent-mines cell))))))
      (println))))

(defn print-status [state]
  (let [flags (count-flags state)
        remaining (- (:mines-count state) flags)]
    (println (format "\n💣 Minas: %d  |  🚩 Bandeiras: %d  |  Restantes: %d"
                     (:mines-count state) flags remaining))))

(defn print-game-over [state]
  (if (:won state)
    (println "\n🎉 PARABÉNS! Você venceu! 🎉")
    (println "\n💥 BOOM! Você perdeu! 💥")))

(defn print-welcome []
  (println "==================================================")
  (println "        🎮 CAMPO MINADO 💣")
  (println "==================================================")
  (println "\nBem-vindo ao Campo Minado!")
  (println "Revele todas as células sem minas para vencer.")
  (println "\nInstruções:")
  (println "  - Digite 'r <linha> <coluna>' para revelar uma célula")
  (println "  - Digite 'f <linha> <coluna>' para marcar/desmarcar bandeira")
  (println "  - Digite 'q' para sair")
  (println "\nNúmeros indicam quantas minas estão adjacentes.")
  (println "=================================================="))

(defn print-error [message]
  (println (format "\n❌ %s" message)))

(defn get-move []
  (println "\nAções: r <linha> <coluna> = revelar | f <linha> <coluna> = bandeira | q = sair")
  (print "Seu movimento: ")
  (flush)
  (when-let [input (read-line)]
    (let [parts (str/split (str/trim input) #"\s+")]
      (cond
        (empty? parts) nil
        (= "q" (first parts)) [:quit]
        (and (#{"r" "f"} (first parts))
             (= 3 (count parts)))
        (try
          (let [action (keyword (first parts))
                row (Integer/parseInt (second parts))
                col (Integer/parseInt (nth parts 2))]
            [action row col])
          (catch Exception _ nil))
        :else nil))))

(defn game-loop [state]
  (if (:game-over state)
    state
    (do
      (clear-screen)
      (print-board state)
      (print-status state)
      (let [move (get-move)]
        (cond
          (nil? move)
          (do
            (print-error "Movimento inválido!")
            (println "Pressione ENTER para continuar...")
            (read-line)
            (recur state))
          (= [:quit] move)
          (do
            (println "\nSaindo ...")
            state)
          :else
          (let [[action row col] move
                new-state (case action
                           :r (reveal-cell state row col)
                           :f (toggle-flag state row col)
                           state)]
            (recur new-state)))))))

(defn -main []
  (print-welcome)
  (let [width 8
        height 8
        mines 10
        initial-state (init-game width height mines)
        final-state (game-loop initial-state)]
    (when (:game-over final-state)
      (clear-screen)
      (print-board final-state)
      (print-status final-state)
      (print-game-over final-state)
      (println))))

(-main)
